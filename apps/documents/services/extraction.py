import hashlib
import logging
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.documents.models import ExtractedText, UploadedDocument

logger = logging.getLogger(__name__)


def calculate_file_hash(file):
    hasher = hashlib.sha256()
    file.seek(0)
    for chunk in file.chunks():
        hasher.update(chunk)
    file.seek(0)
    return hasher.hexdigest()


def validate_document_file(file):
    max_bytes = int(settings.DOCUMENT_MAX_UPLOAD_MB * 1024 * 1024)
    if file.size <= 0:
        raise ValidationError("Empty files are not allowed.")
    if file.size > max_bytes:
        raise ValidationError(f"File exceeds {settings.DOCUMENT_MAX_UPLOAD_MB}MB limit.")

    ext = Path(file.name).suffix.lower().lstrip(".")
    allowed = [e.strip().lower() for e in settings.ALLOWED_DOCUMENT_EXTENSIONS]
    if ext not in allowed:
        raise ValidationError("Unsupported file type.")
    return ext


def classify_document_file(uploaded_document):
    return uploaded_document.file_type


def extract_text_from_pdf(uploaded_document):
    file_path = uploaded_document.file.path

    try:
        import fitz

        with fitz.open(file_path) as doc:
            text_parts = [page.get_text("text") for page in doc]
            text = "\n".join(part.strip() for part in text_parts if part and part.strip()).strip()
            return text, ExtractedText.Method.PYMUPDF, len(doc)
    except ImportError:
        logger.info("PyMuPDF unavailable, falling back to pdfplumber")
    except Exception:
        logger.exception("PyMuPDF extraction failed")

    import pdfplumber

    with pdfplumber.open(file_path) as pdf:
        text_parts = [(page.extract_text() or "") for page in pdf.pages]
        text = "\n".join(part.strip() for part in text_parts if part and part.strip()).strip()
        return text, ExtractedText.Method.PDFPLUMBER, len(pdf.pages)


def extract_text(uploaded_document):
    file_type = classify_document_file(uploaded_document)
    if file_type != UploadedDocument.FileType.PDF:
        message = "Image OCR support will be added in a later milestone."
        uploaded_document.status = UploadedDocument.Status.EXTRACTION_FAILED
        uploaded_document.extraction_error = message
        uploaded_document.save(update_fields=["status", "extraction_error", "updated_at"])
        return None

    text, method, page_count = extract_text_from_pdf(uploaded_document)
    if not text:
        message = "No extractable text found. Scanned document support will be added later."
        uploaded_document.status = UploadedDocument.Status.EXTRACTION_FAILED
        uploaded_document.extraction_error = message
        uploaded_document.save(update_fields=["status", "extraction_error", "updated_at"])
        return None

    extracted, _ = ExtractedText.objects.update_or_create(
        document=uploaded_document,
        defaults={
            "extraction_method": method,
            "text": text,
            "page_count": page_count,
            "metadata": {},
        },
    )
    uploaded_document.status = UploadedDocument.Status.EXTRACTED
    uploaded_document.extraction_error = ""
    uploaded_document.save(update_fields=["status", "extraction_error", "updated_at"])
    return extracted

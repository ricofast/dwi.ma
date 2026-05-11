from datetime import datetime
from uuid import UUID

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ninja import File, Form, Router
from ninja.files import UploadedFile
from ninja.errors import HttpError
from pydantic import BaseModel

from apps.documents.models import UploadedDocument
from apps.documents.services.extraction import calculate_file_hash, extract_text, validate_document_file

router = Router(tags=["documents"])


class DocumentOut(BaseModel):
    document_id: UUID
    status: str
    filename: str
    file_type: str
    file_size: int


@router.post("/documents/upload", response=DocumentOut)
def upload_document(request, file: UploadedFile = File(...), consent_accepted: bool = Form(False), source: str = Form("pwa")):
    if not request.user.is_authenticated:
        raise HttpError(401, "Authentication required")
    if not consent_accepted:
        raise HttpError(400, "Privacy consent is required")
    try:
        file_type = validate_document_file(file)
    except ValidationError as exc:
        raise HttpError(400, "; ".join(exc.messages))

    document = UploadedDocument.objects.create(
        user=request.user,
        original_filename=file.name,
        file=file,
        file_type=file_type,
        file_size=file.size,
        sha256_hash=calculate_file_hash(file),
        source=source,
        status=UploadedDocument.Status.UPLOADED,
    )
    return DocumentOut(
        document_id=document.id,
        status=document.status,
        filename=document.original_filename,
        file_type=document.file_type,
        file_size=document.file_size,
    )


@router.get("/documents/{document_id}")
def get_document(request, document_id: UUID):
    if not request.user.is_authenticated:
        raise HttpError(401, "Authentication required")
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    return {
        "document_id": doc.id,
        "status": doc.status,
        "filename": doc.original_filename,
        "file_type": doc.file_type,
        "file_size": doc.file_size,
        "source": doc.source,
        "deleted_at": doc.deleted_at,
        "created_at": doc.created_at,
    }


def _extract_document(request, document_id: UUID):
    if not request.user.is_authenticated:
        raise HttpError(401, "Authentication required")
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    doc.status = UploadedDocument.Status.EXTRACTING
    doc.save(update_fields=["status", "updated_at"])
    extract_text(doc)
    doc.refresh_from_db()
    return {"document_id": str(doc.id), "status": doc.status}


@router.post("/documents/{document_id}/extract")
@router.post("/documents/{document_id}/extract/")
@router.get("/documents/{document_id}/extract")
@router.get("/documents/{document_id}/extract/")
def extract_document(request, document_id: UUID):
    return _extract_document(request, document_id)


@router.get("/documents/{document_id}/extracted-text")
def get_extracted_text(request, document_id: UUID):
    if not request.user.is_authenticated:
        raise HttpError(401, "Authentication required")
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    if not hasattr(doc, "extracted_text"):
        raise HttpError(404, "Extracted text not available")
    return {
        "document_id": str(doc.id),
        "status": doc.status,
        "extraction_method": doc.extracted_text.extraction_method,
        "text": doc.extracted_text.text,
        "page_count": doc.extracted_text.page_count,
    }


@router.delete("/documents/{document_id}")
def delete_document(request, document_id: UUID):
    if not request.user.is_authenticated:
        raise HttpError(401, "Authentication required")
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    storage = doc.file.storage
    file_name = doc.file.name
    if file_name and storage.exists(file_name):
        storage.delete(file_name)
    doc.mark_deleted()
    return {"status": "deleted", "deleted_at": datetime.utcnow().isoformat()}

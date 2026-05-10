import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class UploadedDocument(models.Model):
    class Source(models.TextChoices):
        PWA = "pwa", "PWA"
        WHATSAPP = "whatsapp", "WhatsApp"
        ADMIN = "admin", "Admin"

    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        EXTRACTING = "extracting", "Extracting"
        EXTRACTED = "extracted", "Extracted"
        EXTRACTION_FAILED = "extraction_failed", "Extraction Failed"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        DELETED = "deleted", "Deleted"

    class FileType(models.TextChoices):
        PDF = "pdf", "PDF"
        JPG = "jpg", "JPG"
        JPEG = "jpeg", "JPEG"
        PNG = "png", "PNG"
        WEBP = "webp", "WEBP"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uploaded_documents")
    original_filename = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/%Y/%m/%d/")
    file_type = models.CharField(max_length=16, choices=FileType.choices)
    file_size = models.PositiveBigIntegerField()
    sha256_hash = models.CharField(max_length=64)
    source = models.CharField(max_length=16, choices=Source.choices, default=Source.PWA)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.UPLOADED)
    extraction_error = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "status", "created_at"]),
            models.Index(fields=["sha256_hash"]),
        ]

    def mark_deleted(self):
        self.status = self.Status.DELETED
        self.deleted_at = timezone.now()
        self.save(update_fields=["status", "deleted_at", "updated_at"])


class ExtractedText(models.Model):
    class Method(models.TextChoices):
        PYMUPDF = "pymupdf", "PyMuPDF"
        PDFPLUMBER = "pdfplumber", "pdfplumber"
        PYPDF = "pypdf", "pypdf"
        OCR = "ocr", "OCR"
        VISION_LLM = "vision_llm", "Vision LLM"
        MANUAL = "manual", "Manual"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.OneToOneField(UploadedDocument, on_delete=models.CASCADE, related_name="extracted_text")
    extraction_method = models.CharField(max_length=32, choices=Method.choices)
    text = models.TextField()
    page_count = models.PositiveIntegerField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

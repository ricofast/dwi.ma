import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadedDocument",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("original_filename", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to="documents/%Y/%m/%d/")),
                ("file_type", models.CharField(choices=[("pdf", "PDF"), ("jpg", "JPG"), ("jpeg", "JPEG"), ("png", "PNG"), ("webp", "WEBP")], max_length=16)),
                ("file_size", models.PositiveBigIntegerField()),
                ("sha256_hash", models.CharField(max_length=64)),
                ("source", models.CharField(choices=[("pwa", "PWA"), ("whatsapp", "WhatsApp"), ("admin", "Admin")], default="pwa", max_length=16)),
                ("status", models.CharField(choices=[("uploaded", "Uploaded"), ("extracting", "Extracting"), ("extracted", "Extracted"), ("extraction_failed", "Extraction Failed"), ("processing", "Processing"), ("completed", "Completed"), ("failed", "Failed"), ("deleted", "Deleted")], default="uploaded", max_length=32)),
                ("extraction_error", models.TextField(blank=True, null=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="uploaded_documents", to=settings.AUTH_USER_MODEL)),
            ],
            options={"indexes": [models.Index(fields=["user", "status", "created_at"], name="documents_upl_user_id_2819b7_idx"), models.Index(fields=["sha256_hash"], name="documents_upl_sha256__5f49fd_idx")]},
        ),
        migrations.CreateModel(
            name="ExtractedText",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("extraction_method", models.CharField(choices=[("pymupdf", "PyMuPDF"), ("pdfplumber", "pdfplumber"), ("pypdf", "pypdf"), ("ocr", "OCR"), ("vision_llm", "Vision LLM"), ("manual", "Manual")], max_length=32)),
                ("text", models.TextField()),
                ("page_count", models.PositiveIntegerField(blank=True, null=True)),
                ("confidence", models.FloatField(blank=True, null=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("document", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="extracted_text", to="documents.uploadeddocument")),
            ],
        ),
    ]

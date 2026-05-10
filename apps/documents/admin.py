from django.contrib import admin

from .models import ExtractedText, UploadedDocument


@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "original_filename",
        "file_type",
        "file_size",
        "status",
        "source",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    list_filter = ("status", "file_type", "source", "created_at")
    search_fields = ("original_filename", "sha256_hash", "user__phone_number")


@admin.register(ExtractedText)
class ExtractedTextAdmin(admin.ModelAdmin):
    list_display = ("document", "extraction_method", "page_count", "created_at", "updated_at")
    list_filter = ("extraction_method", "created_at")

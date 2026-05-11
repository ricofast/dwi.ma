from django.contrib import admin

from .models import DocumentAnalysis, ExtractedText, UploadedDocument


@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ("user", "original_filename", "file_type", "status", "created_at")
    list_filter = ("status", "file_type", "source", "created_at")


@admin.register(ExtractedText)
class ExtractedTextAdmin(admin.ModelAdmin):
    list_display = ("document", "extraction_method", "page_count", "created_at")


@admin.register(DocumentAnalysis)
class DocumentAnalysisAdmin(admin.ModelAdmin):
    list_display = ("document", "ai_job", "document_type", "created_at")

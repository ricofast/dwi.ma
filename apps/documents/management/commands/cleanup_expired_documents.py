from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.documents.models import UploadedDocument

class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=settings.DOCUMENT_ORIGINAL_RETENTION_DAYS)
        for d in UploadedDocument.objects.filter(created_at__lt=cutoff, deleted_at__isnull=True):
            if d.file and d.file.name and d.file.storage.exists(d.file.name):
                d.file.storage.delete(d.file.name)
            if settings.DELETE_EXTRACTED_TEXT_ON_DOCUMENT_DELETE and hasattr(d, 'extracted_text'):
                d.extracted_text.text = ''
                d.extracted_text.save(update_fields=['text', 'updated_at'])

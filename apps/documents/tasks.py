import logging

from celery import shared_task

from apps.documents.models import UploadedDocument
from apps.documents.services.extraction import extract_text

logger = logging.getLogger(__name__)


@shared_task
def extract_document_text_task(document_id):
    document = UploadedDocument.objects.get(id=document_id)
    document.status = UploadedDocument.Status.EXTRACTING
    document.save(update_fields=["status", "updated_at"])
    try:
        extract_text(document)
    except Exception as exc:
        logger.exception("Document extraction failed")
        document.status = UploadedDocument.Status.EXTRACTION_FAILED
        document.extraction_error = str(exc)
        document.save(update_fields=["status", "extraction_error", "updated_at"])

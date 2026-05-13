from django.conf import settings
from apps.core.services.audit import log_action
from apps.documents.models import UploadedDocument


def _delete_file(field_file):
    if field_file and field_file.name and field_file.storage.exists(field_file.name):
        field_file.storage.delete(field_file.name)


def delete_document_for_user(document, user):
    if document.user_id != user.id:
        raise PermissionError("Not allowed")
    _delete_file(document.file)
    if getattr(settings, "DELETE_EXTRACTED_TEXT_ON_DOCUMENT_DELETE", True) and hasattr(document, "extracted_text"):
        document.extracted_text.text = ""
        document.extracted_text.save(update_fields=["text", "updated_at"])
    document.mark_deleted()
    log_action(actor=user, action="document_deleted", target=document)
    return document


def admin_delete_document(document, admin_user, reason=None):
    _delete_file(document.file)
    document.mark_deleted()
    log_action(actor=admin_user, action="admin_document_deleted", target=document, metadata={"reason": reason or ""})
    return document

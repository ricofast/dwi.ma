from celery import shared_task

from django.contrib.auth import get_user_model

from apps.documents.services.analysis import explain_document


@shared_task
def explain_document_task(self, document_id, user_id):
    user = get_user_model().objects.get(id=user_id)
    return str(explain_document(document_id, user).id)

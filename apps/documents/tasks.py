from celery import shared_task

from django.contrib.auth import get_user_model

from apps.documents.services.analysis import explain_document
from apps.assistant.models import AIJob

@shared_task(name='document_explanation', bind=True, max_retries=3)
def explain_document_task(document_id, user_id):
    user = get_user_model().objects.get(id=user_id)
    return str(explain_document(document_id, user).id)


def explain_all_documents_task():
    jobs = AIJob.objects.filter(status=AIJob.Status.QUEUED)

    for job in jobs:
        pass
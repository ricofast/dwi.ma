from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from config.celery import app
from apps.assistant.models import AIJob
from apps.assistant.services.text_explanation import explain_text


@app.task(bind=True)
def explain_text_task(self, user_id, input_text, options=None):
    options = options or {}
    user = get_user_model().objects.filter(id=user_id).first()
    if not user:
        raise ValidationError("User not found")
    job = AIJob.objects.filter(id=options.get("job_id"), user=user).first() if options.get("job_id") else None
    result = explain_text(user=user, input_text=input_text, user_instruction=options.get("instructions"),
                          output_language=options.get("output_language", "darija_arabic"), ai_job=job)
    return str(result["job"].id)

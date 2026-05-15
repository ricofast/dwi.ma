from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from pydantic import BaseModel
from django.conf import settings
from apps.accounts.auth import require_auth
from apps.assistant.models import AIJob
import hashlib
from apps.assistant.tasks import explain_text_task
from apps.wallet.services import can_spend

router = Router(tags=["assistant"])


class ExplainTextIn(BaseModel):
    text: str
    output_language: str = "darija_arabic"


@router.post("/assistant/explain-text")
def explain_text_endpoint(request, payload: ExplainTextIn):
    require_auth(request)
    amount = int(getattr(settings, "CREDITS_COST_TEXT_EXPLANATION", 1))
    if not payload.text or len(payload.text.strip()) < 10:
        raise HttpError(400, "النص خاص يكون فيه على الأقل 10 حروف")
    if not can_spend(request.user, amount):
        raise HttpError(402, "Insufficient credits")
    text = payload.text.strip()
    job = AIJob.objects.create(user=request.user, job_type=AIJob.JobType.TEXT_EXPLANATION, provider="", model="", status=AIJob.Status.QUEUED, input_hash=hashlib.sha256(text.encode()).hexdigest(), input_preview=text[:500], prompt_version="")
    explain_text_task.delay(str(request.user.id), text, {"output_language": payload.output_language, "job_id": str(job.id)})
    return {"job_id": str(job.id), "status": "queued"}


@router.get("/assistant/text-explanations/{job_id}")
def text_explanation_result(request, job_id: UUID):
    require_auth(request)
    job = get_object_or_404(AIJob, id=job_id, user=request.user, job_type=AIJob.JobType.TEXT_EXPLANATION)
    if job.status != AIJob.Status.COMPLETED or not job.result_json:
        return {"job_id": str(job.id), "status": job.status}
    data = job.result_json
    return {
        "job_id": str(job.id),
        "status": job.status,
        "text_type": data.get("text_type", ""),
        "summary_darija": data.get("short_summary_darija", ""),
        "important_points": data.get("important_points_darija", []),
        "extracted_entities": data.get("extracted_entities", {}),
        "unclear_points": data.get("unclear_points_darija", []),
        "next_steps": data.get("next_steps_darija", []),
        "disclaimer": data.get("disclaimer_darija", ""),
        "full_answer": data.get("full_answer_darija", ""),
    }


class GenerateMessageIn(BaseModel):
    input_text: str
    target_format: str
    tone: str = "polite"


@router.post("/assistant/generate-message")
def generate_message_endpoint(request, payload: GenerateMessageIn):
    require_auth(request)
    from apps.assistant.services.message_generation import generate_message_from_text
    res = generate_message_from_text(request.user, payload.input_text, payload.target_format, payload.tone)
    return {"job_id": str(res["job"].id), "status": res["job"].status}


@router.get("/assistant/message-generations/{job_id}")
def message_generation_result(request, job_id: UUID):
    require_auth(request)
    job = get_object_or_404(AIJob, id=job_id, user=request.user, job_type=AIJob.JobType.MESSAGE_GENERATION)
    data = job.result_json or {}
    return {"job_id": str(job.id), "status": job.status, "detected_intent": data.get("detected_intent", ""), "missing_information": data.get("missing_information", []), "generated_message": data.get("generated_message", ""), "suggested_subject": data.get("suggested_subject", ""), "notes_darija": data.get("notes_darija", "")}


class FeedbackIn(BaseModel):
    rating: str
    comment: str = ""

@router.post("/assistant/jobs/{job_id}/feedback")
def submit_feedback(request, job_id: UUID, payload: FeedbackIn):
    require_auth(request)
    job = get_object_or_404(AIJob, id=job_id, user=request.user)
    from apps.assistant.models import UserFeedback
    fb, _ = UserFeedback.objects.update_or_create(user=request.user, ai_job=job, defaults={"rating": payload.rating, "comment": payload.comment})
    return {"status": "ok", "feedback_id": str(fb.id)}

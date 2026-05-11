from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from pydantic import BaseModel

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
    if not payload.text or len(payload.text.strip()) < 10:
        raise HttpError(400, "النص خاص يكون فيه على الأقل 10 حروف")
    if not can_spend(request.user, 1):
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

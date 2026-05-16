import hashlib

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from apps.assistant.models import AIJob, AIResponse
from apps.assistant.services.providers import generate_document_explanation
from apps.documents.models import DocumentAnalysis, UploadedDocument
from apps.wallet.services import charge_reserved_usage, fail_usage, reserve_credits


def explain_document(document_id, user):
    document = UploadedDocument.objects.filter(id=document_id, user=user).first()
    print(document.id)
    if not document:
        raise ValidationError("Document not found")
    if not hasattr(document, "extracted_text"):
        raise ValidationError("ماعندناش النص المستخرج من هاد الوثيقة دابا.")
    if document.status != UploadedDocument.Status.EXTRACTED:
        raise ValidationError("الوثيقة خاصها تكون واجدة للشرح.")

    amount = int(getattr(settings, "CREDITS_COST_DOCUMENT_EXPLANATION", 2))

    usage = reserve_credits(user=user, amount=amount, event_type="document_explanation", reference_type="document", reference_id=document.id)
    ai_job = AIJob.objects.create(user=user, job_type=AIJob.JobType.DOCUMENT_EXPLANATION, provider="", model="", status=AIJob.Status.QUEUED, input_hash=hashlib.sha256(document.extracted_text.text.encode()).hexdigest(), input_preview=document.extracted_text.text[:500], prompt_version="")
    try:
        ai_job.status = AIJob.Status.RUNNING
        document.status = UploadedDocument.Status.PROCESSING
        ai_job.save(update_fields=["status", "updated_at"])
        document.save(update_fields=["status", "updated_at"])
        print("*************************************************************************")
        print(document.extracted_text.text)
        print("*************************************************************************")
        res = generate_document_explanation(document.extracted_text.text)
        ai_job.provider = res["provider"]
        ai_job.model = res["model"]
        ai_job.prompt_version = res["prompt_version"]
        ai_job.result_json = res["parsed_json"]
        ai_job.result_text = res["raw_response_text"]
        ai_job.status = AIJob.Status.COMPLETED
        ai_job.completed_at = timezone.now()
        ai_job.save()
        AIResponse.objects.create(ai_job=ai_job, raw_response_text=res["raw_response_text"], parsed_json=res["parsed_json"])
        p = res["parsed_json"]
        analysis = DocumentAnalysis.objects.create(document=document, ai_job=ai_job, document_type=p.get("document_type", ""), summary_darija=p.get("short_summary_darija", ""), important_points_json=p.get("important_points_darija", []), extracted_entities_json=p.get("extracted_entities", {}), unclear_points_json=p.get("unclear_points_darija", []), next_steps_json=p.get("next_steps_darija", []), disclaimer_darija=p.get("disclaimer_darija", ""), full_response_text=p.get("full_answer_darija", ""))
        document.status = UploadedDocument.Status.COMPLETED
        document.save(update_fields=["status", "updated_at"])
        charge_reserved_usage(usage)
        return analysis
    except Exception:
        ai_job.status = AIJob.Status.FAILED
        ai_job.error_message = "تعذر توليد الشرح دابا، حاول من بعد."
        ai_job.completed_at = timezone.now()
        ai_job.save(update_fields=["status", "error_message", "completed_at", "updated_at"])
        document.status = UploadedDocument.Status.FAILED
        document.save(update_fields=["status", "updated_at"])
        fail_usage(usage, reason="llm_failed")
        raise ValidationError("تعذر توليد الشرح دابا، حاول من بعد.")

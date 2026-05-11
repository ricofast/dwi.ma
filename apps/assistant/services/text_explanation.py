import hashlib
import json

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.assistant.models import AIJob, AIResponse, PromptTemplate, TextExplanation
from apps.assistant.services.providers import _get_provider
from apps.wallet.services import reserve_credits, charge_reserved_usage, fail_usage

REQUIRED_KEYS = {
    "text_type",
    "short_summary_darija",
    "important_points_darija",
    "extracted_entities",
    "unclear_points_darija",
    "next_steps_darija",
    "disclaimer_darija",
    "full_answer_darija",
}


def explain_text(user, input_text, output_language="darija_arabic", ai_job=None):
    if not user or not user.is_authenticated:
        raise ValidationError("Authentication required")
    text = (input_text or "").strip()
    if not text:
        raise ValidationError("المرجو لسق نص باش نشرحو ليك.")
    if len(text) < 10:
        raise ValidationError("النص قصير بزاف، خاص يكون فيه على الأقل 10 حروف.")
    max_chars = int(getattr(settings, "TEXT_EXPLANATION_MAX_CHARS", 12000))
    if len(text) > max_chars:
        raise ValidationError("النص طويل بزاف، نقصو شوية وحاول مرة أخرى.")

    tmpl = PromptTemplate.objects.filter(name="text_explanation", active=True).order_by("-updated_at").first()
    if not tmpl:
        raise ValidationError("Prompt template unavailable")

    usage = reserve_credits(user=user, amount=1, event_type="text_explanation", reference_type="text")
    provider_name = getattr(settings, "DEFAULT_LLM_PROVIDER", "mock")
    model_name = getattr(settings, "DEFAULT_LLM_MODEL", "mock-1")
    job = ai_job or AIJob.objects.create(
        user=user,
        job_type=AIJob.JobType.TEXT_EXPLANATION,
        provider=provider_name,
        model=model_name,
        status=AIJob.Status.QUEUED,
        input_hash=hashlib.sha256(text.encode()).hexdigest(),
        input_preview=text[:500],
        prompt_version=tmpl.version,
    )
    if ai_job:
        job.provider = provider_name
        job.model = model_name
        job.input_hash = hashlib.sha256(text.encode()).hexdigest()
        job.input_preview = text[:500]
        job.prompt_version = tmpl.version
        job.save(update_fields=["provider", "model", "input_hash", "input_preview", "prompt_version", "updated_at"])

    def parse_payload(raw):
        try:
            data = json.loads(raw)
        except Exception:
            return None
        return data if REQUIRED_KEYS.issubset(set(data.keys())) else None

    try:
        job.status = AIJob.Status.RUNNING
        job.save(update_fields=["status", "updated_at"])
        provider = _get_provider(provider_name)
        user_prompt = tmpl.user_prompt_template.replace("{{input_text}}", text)
        raw = provider.generate(tmpl.system_prompt, user_prompt, model_name)
        parsed = parse_payload(raw)
        if parsed is None:
            raw = provider.generate("You repair invalid JSON outputs. Return valid JSON only.", f"Repair JSON: {raw}", model_name)
            parsed = parse_payload(raw)
        if parsed is None:
            raise ValidationError("تعذر فهم النتيجة، حاول من بعد.")

        AIResponse.objects.update_or_create(ai_job=job, defaults={"raw_response_text": raw, "parsed_json": parsed})
        TextExplanation.objects.create(
            user=user,
            ai_job=job,
            original_text=text,
            detected_text_type=parsed.get("text_type", ""),
            summary_darija=parsed.get("short_summary_darija", ""),
            important_points_json=parsed.get("important_points_darija", []),
            extracted_entities_json=parsed.get("extracted_entities", {}),
            unclear_points_json=parsed.get("unclear_points_darija", []),
            next_steps_json=parsed.get("next_steps_darija", []),
            disclaimer_darija=parsed.get("disclaimer_darija", ""),
            full_response_text=parsed.get("full_answer_darija", ""),
        )
        job.result_json = parsed
        job.result_text = raw
        job.status = AIJob.Status.COMPLETED
        job.completed_at = timezone.now()
        job.save()
        charge_reserved_usage(usage)
        return {"job": job, "result": parsed}
    except Exception:
        job.status = AIJob.Status.FAILED
        job.error_message = "تعذر توليد الشرح دابا، حاول من بعد."
        job.completed_at = timezone.now()
        job.save(update_fields=["status", "error_message", "completed_at", "updated_at"])
        fail_usage(usage, reason="text_explanation_failed")
        raise ValidationError("تعذر توليد الشرح دابا، حاول من بعد.")

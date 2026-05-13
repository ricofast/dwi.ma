import hashlib
import json
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.assistant.models import AIJob, AIResponse, MessageGeneration, PromptTemplate
from apps.assistant.services.providers import _get_provider
from apps.wallet.services import reserve_credits, charge_reserved_usage, fail_usage

ALLOWED_FORMATS = [c[0] for c in MessageGeneration.TargetFormat.choices]
ALLOWED_TONES = [c[0] for c in MessageGeneration.Tone.choices]
REQ_KEYS = {"detected_intent", "missing_information", "generated_message", "suggested_subject", "notes_darija"}


def generate_message_from_text(user, input_text, target_format, tone="polite", voice_note=None, transcription_job=None):
    if not user or not user.is_authenticated:
        raise ValidationError("Authentication required")
    text = (input_text or "").strip()
    if not text:
        raise ValidationError("المرجو تدخل محتوى الرسالة.")
    if target_format not in ALLOWED_FORMATS:
        raise ValidationError("Invalid target format")
    if tone not in ALLOWED_TONES:
        raise ValidationError("Invalid tone")

    tmpl = PromptTemplate.objects.filter(name="message_generation", active=True).order_by("-updated_at").first()
    if not tmpl:
        raise ValidationError("Prompt template unavailable")

    usage = reserve_credits(user=user, amount=1, event_type="message_generation", reference_type="text")
    provider_name = getattr(settings, "DEFAULT_LLM_PROVIDER", "mock")
    model_name = getattr(settings, "DEFAULT_LLM_MODEL", "mock-1")
    job = AIJob.objects.create(user=user, job_type=AIJob.JobType.MESSAGE_GENERATION, provider=provider_name, model=model_name, status=AIJob.Status.QUEUED, input_hash=hashlib.sha256(text.encode()).hexdigest(), input_preview=text[:500], prompt_version=tmpl.version)

    def parse(s):
        try:
            data = json.loads(s)
            return data if REQ_KEYS.issubset(data.keys()) else None
        except Exception:
            return None

    try:
        job.status = AIJob.Status.RUNNING; job.save(update_fields=["status", "updated_at"])
        user_prompt = tmpl.user_prompt_template.replace("{{input_text}}", text).replace("{{target_format}}", target_format).replace("{{tone}}", tone)
        provider = _get_provider(provider_name)
        raw = provider.generate(tmpl.system_prompt, user_prompt, model_name)
        parsed = parse(raw)
        if parsed is None:
            raw = provider.generate("Return JSON only.", f"Repair this into valid JSON with required schema: {raw}", model_name)
            parsed = parse(raw)
        if parsed is None:
            raise ValidationError("invalid json")

        AIResponse.objects.update_or_create(ai_job=job, defaults={"raw_response_text": raw, "parsed_json": parsed})
        MessageGeneration.objects.create(user=user, ai_job=job, voice_note=voice_note, transcription_job=transcription_job, input_text=text, target_format=target_format, tone=tone, generated_message=parsed.get("generated_message", ""))
        job.status = AIJob.Status.COMPLETED; job.result_json = parsed; job.result_text = raw; job.completed_at = timezone.now(); job.save()
        charge_reserved_usage(usage)
        return {"job": job, "result": parsed}
    except Exception:
        job.status = AIJob.Status.FAILED; job.error_message = "تعذر توليد الرسالة حاليا، حاول من بعد."; job.completed_at = timezone.now(); job.save(update_fields=["status", "error_message", "completed_at", "updated_at"])
        fail_usage(usage, reason="message_generation_failed")
        raise ValidationError("تعذر توليد الرسالة حاليا، حاول من بعد.")

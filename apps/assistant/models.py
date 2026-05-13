import uuid

from django.conf import settings
from django.db import models


class AIJob(models.Model):
    class JobType(models.TextChoices):
        DOCUMENT_EXPLANATION = "document_explanation", "Document Explanation"
        TEXT_EXPLANATION = "text_explanation", "Text Explanation"
        MESSAGE_GENERATION = "message_generation", "Message Generation"
        INTENT_DETECTION = "intent_detection", "Intent Detection"

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_jobs")
    job_type = models.CharField(max_length=32, choices=JobType.choices)
    provider = models.CharField(max_length=64)
    model = models.CharField(max_length=128)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.QUEUED)
    input_hash = models.CharField(max_length=64)
    input_preview = models.TextField()
    prompt_version = models.CharField(max_length=64)
    result_json = models.JSONField(null=True, blank=True)
    result_text = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    latency_ms = models.PositiveIntegerField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PromptTemplate(models.Model):
    name = models.CharField(max_length=128)
    version = models.CharField(max_length=32)
    system_prompt = models.TextField()
    user_prompt_template = models.TextField()
    output_schema = models.JSONField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AIResponse(models.Model):
    ai_job = models.OneToOneField(AIJob, on_delete=models.CASCADE, related_name="response")
    raw_response_text = models.TextField()
    parsed_json = models.JSONField(null=True, blank=True)
    provider_response_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SafetyFlag(models.Model):
    class FlagType(models.TextChoices):
        LEGAL = "legal", "Legal"
        MEDICAL = "medical", "Medical"
        FINANCIAL = "financial", "Financial"
        ADMINISTRATIVE = "administrative", "Administrative"
        UNCLEAR = "unclear", "Unclear"
        HALLUCINATION_RISK = "hallucination_risk", "Hallucination Risk"
        UNSAFE = "unsafe", "Unsafe"

    ai_job = models.ForeignKey(AIJob, on_delete=models.CASCADE, related_name="safety_flags")
    flag_type = models.CharField(max_length=32, choices=FlagType.choices)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class TextExplanation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="text_explanations")
    ai_job = models.ForeignKey(AIJob, on_delete=models.CASCADE, related_name="text_explanations")
    original_text = models.TextField()
    detected_text_type = models.CharField(max_length=128, null=True, blank=True)
    summary_darija = models.TextField(blank=True, default="")
    important_points_json = models.JSONField(default=list, blank=True)
    extracted_entities_json = models.JSONField(default=dict, blank=True)
    unclear_points_json = models.JSONField(default=list, blank=True)
    next_steps_json = models.JSONField(default=list, blank=True)
    disclaimer_darija = models.TextField(blank=True, default="")
    full_response_text = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MessageGeneration(models.Model):
    class TargetFormat(models.TextChoices):
        PROFESSIONAL_FRENCH_EMAIL = "professional_french_email", "Professional French Email"
        PROFESSIONAL_ARABIC_MESSAGE = "professional_arabic_message", "Professional Arabic Message"
        POLISHED_DARIJA_WHATSAPP = "polished_darija_whatsapp", "Polished Darija WhatsApp"
        SHORT_REPLY = "short_reply", "Short Reply"

    class Tone(models.TextChoices):
        NEUTRAL = "neutral", "Neutral"
        POLITE = "polite", "Polite"
        POLITE_FIRM = "polite_firm", "Polite Firm"
        FRIENDLY = "friendly", "Friendly"
        FORMAL = "formal", "Formal"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="message_generations")
    ai_job = models.ForeignKey(AIJob, on_delete=models.CASCADE, related_name="message_generations")
    voice_note = models.ForeignKey("audio.VoiceNote", null=True, blank=True, on_delete=models.SET_NULL, related_name="message_generations")
    transcription_job = models.ForeignKey("audio.TranscriptionJob", null=True, blank=True, on_delete=models.SET_NULL, related_name="message_generations")
    input_text = models.TextField()
    target_format = models.CharField(max_length=64, choices=TargetFormat.choices)
    tone = models.CharField(max_length=32, choices=Tone.choices, default=Tone.POLITE)
    generated_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

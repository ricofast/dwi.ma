import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class VoiceNote(models.Model):
    class Source(models.TextChoices):
        PWA = "pwa", "PWA"
        WHATSAPP = "whatsapp", "WhatsApp"
        ADMIN = "admin", "Admin"

    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        TRANSCRIBING = "transcribing", "Transcribing"
        TRANSCRIBED = "transcribed", "Transcribed"
        TRANSCRIPTION_FAILED = "transcription_failed", "Transcription Failed"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        DELETED = "deleted", "Deleted"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="voice_notes")
    audio_file = models.FileField(upload_to="voice_notes/%Y/%m/%d/")
    original_filename = models.CharField(max_length=255, null=True, blank=True)
    file_type = models.CharField(max_length=32, null=True, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    sha256_hash = models.CharField(max_length=64, null=True, blank=True)
    source = models.CharField(max_length=16, choices=Source.choices, default=Source.PWA)
    whatsapp_media_id = models.CharField(max_length=128, null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.UPLOADED)
    transcription_error = models.TextField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_deleted(self):
        self.status = self.Status.DELETED
        self.deleted_at = timezone.now()
        self.save(update_fields=["status", "deleted_at", "updated_at"])


class TranscriptionJob(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voice_note = models.ForeignKey(VoiceNote, on_delete=models.CASCADE, related_name="transcription_jobs")
    provider = models.CharField(max_length=64)
    model = models.CharField(max_length=128)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.QUEUED)
    transcript = models.TextField(blank=True, default="")
    language_detected = models.CharField(max_length=64, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    raw_response_json = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    latency_ms = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

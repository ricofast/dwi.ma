from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.audio.models import VoiceNote, TranscriptionJob
from apps.audio.services.providers import get_transcription_provider

def transcribe_voice_note(voice_note_id, user=None):
    voice_note = VoiceNote.objects.get(id=voice_note_id)
    if user and voice_note.user_id != user.id: raise ValidationError("Forbidden")
    voice_note.status = VoiceNote.Status.TRANSCRIBING; voice_note.save(update_fields=["status","updated_at"])
    job = TranscriptionJob.objects.create(voice_note=voice_note, provider=getattr(settings,'TRANSCRIPTION_PROVIDER','mock'), model=getattr(settings,'TRANSCRIPTION_MODEL','mock-transcribe'), status=TranscriptionJob.Status.RUNNING)
    try:
        result = get_transcription_provider().transcribe(voice_note.audio_file.path)
        job.transcript=result.get('transcript',''); job.language_detected=result.get('language_detected'); job.confidence=result.get('confidence'); job.raw_response_json=result.get('raw_response_json',{}); job.status=TranscriptionJob.Status.COMPLETED; job.completed_at=timezone.now(); job.save()
        voice_note.status = VoiceNote.Status.TRANSCRIBED; voice_note.transcription_error=''; voice_note.save(update_fields=["status","transcription_error","updated_at"])
        return job
    except Exception:
        msg="Transcription failed"
        job.status=TranscriptionJob.Status.FAILED; job.error_message=msg; job.completed_at=timezone.now(); job.save(update_fields=["status","error_message","completed_at","updated_at"])
        voice_note.status=VoiceNote.Status.TRANSCRIPTION_FAILED; voice_note.transcription_error=msg; voice_note.save(update_fields=["status","transcription_error","updated_at"])
        raise ValidationError(msg)

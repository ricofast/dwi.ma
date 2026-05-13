from django.core.exceptions import ValidationError
from apps.audio.models import VoiceNote, TranscriptionJob
from apps.audio.services.transcription import transcribe_voice_note
from apps.assistant.services.message_generation import generate_message_from_text

def generate_message_from_voice_note(user, voice_note_id, target_format, tone='polite'):
    voice_note = VoiceNote.objects.get(id=voice_note_id, user=user)
    if voice_note.status != VoiceNote.Status.TRANSCRIBED:
        tj = transcribe_voice_note(voice_note.id, user=user)
    else:
        tj = TranscriptionJob.objects.filter(voice_note=voice_note, status=TranscriptionJob.Status.COMPLETED).order_by('-created_at').first()
    if not tj or not tj.transcript:
        raise ValidationError('Transcription unavailable')
    voice_note.status = VoiceNote.Status.PROCESSING; voice_note.save(update_fields=['status','updated_at'])
    res = generate_message_from_text(user=user,input_text=tj.transcript,target_format=target_format,tone=tone,voice_note=voice_note,transcription_job=tj)
    voice_note.status = VoiceNote.Status.COMPLETED; voice_note.save(update_fields=['status','updated_at'])
    return res

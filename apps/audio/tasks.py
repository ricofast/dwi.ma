from django.contrib.auth import get_user_model
from config.celery import app
from apps.audio.services.transcription import transcribe_voice_note
from apps.audio.services.voice_to_message import generate_message_from_voice_note

@app.task(bind=True, max_retries=3)
def transcribe_voice_note_task(self, voice_note_id):
    return str(transcribe_voice_note(voice_note_id).id)

@app.task(bind=True, max_retries=3)
def generate_message_from_voice_note_task(self, user_id, voice_note_id, target_format, tone='polite'):
    user = get_user_model().objects.get(id=user_id)
    return str(generate_message_from_voice_note(user, voice_note_id, target_format, tone=tone)['job'].id)

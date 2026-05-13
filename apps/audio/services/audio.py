import hashlib
from pathlib import Path
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.audio.models import VoiceNote

def calculate_audio_hash(file):
    h = hashlib.sha256()
    pos = file.tell(); file.seek(0)
    for c in file.chunks(): h.update(c)
    file.seek(pos)
    return h.hexdigest()

def validate_audio_file(file):
    if not file or file.size == 0: raise ValidationError("Empty audio file")
    max_bytes = int(getattr(settings, "AUDIO_MAX_UPLOAD_MB", 15)) * 1024 * 1024
    if file.size > max_bytes: raise ValidationError("Audio file too large")
    ext = Path(file.name or "").suffix.lower().replace('.', '')
    allowed = getattr(settings, "ALLOWED_AUDIO_EXTENSIONS", ["mp3","mp4","m4a","wav","webm","ogg","opus"])
    if ext not in allowed: raise ValidationError("Unsupported audio format")
    return ext

def create_voice_note(user, file, source="pwa"):
    ext = validate_audio_file(file)
    return VoiceNote.objects.create(user=user,audio_file=file,original_filename=file.name,file_type=ext,file_size=file.size,sha256_hash=calculate_audio_hash(file),source=source,status=VoiceNote.Status.UPLOADED)

def delete_voice_note(voice_note, user):
    if voice_note.user_id != user.id: raise ValidationError("Forbidden")
    if voice_note.audio_file and voice_note.audio_file.storage.exists(voice_note.audio_file.name): voice_note.audio_file.storage.delete(voice_note.audio_file.name)
    voice_note.mark_deleted(); return voice_note

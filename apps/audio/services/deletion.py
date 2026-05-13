from django.conf import settings
from apps.core.services.audit import log_action


def _delete_file(field_file):
    if field_file and field_file.name and field_file.storage.exists(field_file.name):
        field_file.storage.delete(field_file.name)


def delete_voice_note_for_user(voice_note, user):
    if voice_note.user_id != user.id:
        raise PermissionError("Not allowed")
    _delete_file(voice_note.audio_file)
    if getattr(settings, "DELETE_TRANSCRIPT_ON_AUDIO_DELETE", True):
        for job in voice_note.transcription_jobs.all():
            job.transcript = ""
            job.save(update_fields=["transcript", "updated_at"])
    voice_note.mark_deleted()
    log_action(actor=user, action="voice_note_deleted", target=voice_note)
    return voice_note


def admin_delete_voice_note(voice_note, admin_user, reason=None):
    _delete_file(voice_note.audio_file)
    voice_note.mark_deleted()
    log_action(actor=admin_user, action="admin_voice_note_deleted", target=voice_note, metadata={"reason": reason or ""})
    return voice_note

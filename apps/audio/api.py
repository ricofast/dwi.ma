from uuid import UUID
from django.shortcuts import get_object_or_404
from ninja import File, Form, Router
from ninja.files import UploadedFile
from ninja.errors import HttpError
from pydantic import BaseModel
from apps.accounts.auth import require_auth
from apps.audio.models import VoiceNote, TranscriptionJob
from apps.audio.services.audio import create_voice_note
from apps.audio.services.deletion import delete_voice_note_for_user
from apps.accounts.services.consent import log_consent
from apps.accounts.models import ConsentLog
from apps.audio.services.transcription import transcribe_voice_note
from apps.audio.services.voice_to_message import generate_message_from_voice_note

router = Router(tags=['audio'])
class GenerateIn(BaseModel):
    target_format: str
    tone: str = 'polite'

@router.post('/audio/upload')
def upload_audio(request, file: UploadedFile = File(...), source: str = Form('pwa'), consent_accepted: bool = Form(False)):
    require_auth(request)
    if not consent_accepted:
        raise HttpError(400, "خاصك توافق على معالجة التسجيل الصوتي")
    log_consent(user=request.user, consent_type=ConsentLog.ConsentType.AUDIO_PROCESSING, accepted=True, source=source, request=request, consent_text_snapshot="كنوافق أن dwi.ma يعالج هاد التسجيل الصوتي باش يحولو لنص ويكتب ليا الرسالة.")
    vn = create_voice_note(request.user, file, source=source)
    return {'voice_note_id': str(vn.id), 'status': vn.status, 'filename': vn.original_filename, 'file_size': vn.file_size}

@router.post('/audio/{voice_note_id}/transcribe')
def transcribe(request, voice_note_id: UUID):
    require_auth(request)
    job = transcribe_voice_note(voice_note_id, user=request.user)
    return {'transcription_job_id': str(job.id), 'status': job.status}

@router.get('/audio/{voice_note_id}/transcript')
def transcript(request, voice_note_id: UUID):
    require_auth(request)
    vn = get_object_or_404(VoiceNote, id=voice_note_id, user=request.user)
    tj = TranscriptionJob.objects.filter(voice_note=vn).order_by('-created_at').first()
    if not tj: raise HttpError(404, 'Transcript unavailable')
    return {'voice_note_id': str(vn.id), 'status': vn.status, 'transcript': tj.transcript}

@router.post('/audio/{voice_note_id}/generate-message')
def gen_from_voice(request, voice_note_id: UUID, payload: GenerateIn):
    require_auth(request)
    res = generate_message_from_voice_note(request.user, voice_note_id, payload.target_format, payload.tone)
    return {'job_id': str(res['job'].id), 'voice_note_id': str(voice_note_id), 'status': res['job'].status}

@router.delete('/audio/{voice_note_id}')
def delete_audio(request, voice_note_id: UUID):
    require_auth(request)
    vn = get_object_or_404(VoiceNote, id=voice_note_id, user=request.user)
    delete_voice_note_for_user(vn, request.user)
    return {'status':'deleted'}

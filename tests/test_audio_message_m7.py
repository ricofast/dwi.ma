from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from apps.audio.services.audio import create_voice_note
from apps.audio.services.transcription import transcribe_voice_note
from apps.assistant.services.message_generation import generate_message_from_text
from apps.wallet.models import CreditWallet

class Milestone7Tests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(phone_number='+212600001234', password='x')
        CreditWallet.objects.get_or_create(user=self.user, defaults={'balance': 3})

    @override_settings(ALLOWED_AUDIO_EXTENSIONS=['mp3'], AUDIO_MAX_UPLOAD_MB=1)
    def test_audio_upload_and_transcribe(self):
        f = SimpleUploadedFile('note.mp3', b'abc', content_type='audio/mpeg')
        vn = create_voice_note(self.user, f)
        self.assertEqual(vn.file_type, 'mp3')
        job = transcribe_voice_note(vn.id, user=self.user)
        self.assertEqual(job.status, 'completed')

    def test_generate_message_from_text(self):
        out = generate_message_from_text(self.user, 'بغيت رسالة اعتذار', 'short_reply', 'polite')
        self.assertEqual(out['job'].status, 'completed')
        self.assertIn('generated_message', out['result'])

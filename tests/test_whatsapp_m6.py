from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from apps.accounts.models import WhatsAppIdentity
from apps.assistant.models import AIJob
from apps.whatsapp.models import WhatsAppConversationState, WhatsAppOutboundMessage, WhatsAppWebhookEvent
from apps.whatsapp.services.parser import extract_inbound_messages, normalize_message_type


class WhatsAppM6Tests(TestCase):
    def test_verify_token_valid(self):
        with override_settings(WHATSAPP_VERIFY_TOKEN="abc"):
            r = self.client.get('/api/whatsapp/webhook?hub.verify_token=abc&hub.challenge=123')
            self.assertEqual(r.status_code, 200)

    def test_verify_token_invalid(self):
        with override_settings(WHATSAPP_VERIFY_TOKEN="abc"):
            r = self.client.get('/api/whatsapp/webhook?hub.verify_token=bad&hub.challenge=123')
            self.assertEqual(r.status_code, 403)

    def test_webhook_post_stores_and_no_login(self):
        payload = {"entry": []}
        r = self.client.post('/api/whatsapp/webhook', data=payload, content_type='application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(WhatsAppWebhookEvent.objects.count(), 1)

    def test_parser_types(self):
        self.assertEqual(normalize_message_type({"type":"text"}), "text")
        self.assertEqual(normalize_message_type({"type":"interactive","interactive":{"type":"button_reply"}}), "button")
        self.assertEqual(normalize_message_type({"type":"interactive","interactive":{"type":"list_reply"}}), "list_reply")
        self.assertEqual(normalize_message_type({"type":"sticker"}), "unknown")

    def test_identity_created(self):
        payload = {"entry":[{"changes":[{"value":{"contacts":[{"wa_id":"2126","profile":{"name":"Ali"}}],"messages":[{"from":"2126","id":"m1","type":"text","text":{"body":"salam"}}]}}]}]}
        self.client.post('/api/whatsapp/webhook', data=payload, content_type='application/json')
        self.assertTrue(WhatsAppIdentity.objects.filter(wa_id='2126').exists())

    def test_send_result(self):
        user = get_user_model().objects.create_user(phone_number='+212600000001',password='x')
        self.client.force_login(user)
        WhatsAppIdentity.objects.create(user=user, wa_id='212666', is_linked=True)
        job = AIJob.objects.create(user=user,job_type='text_explanation',provider='x',model='x',status='completed',input_hash='x',input_preview='x',prompt_version='x',result_text='ok')
        r = self.client.post('/api/whatsapp/send-result', data={"job_id": str(job.id)}, content_type='application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(WhatsAppOutboundMessage.objects.count(), 1)

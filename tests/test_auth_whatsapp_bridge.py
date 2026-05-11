from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import WhatsAppIdentity
from apps.accounts.services.magic_links import (
    InvalidMagicToken,
    consume_whatsapp_login_token,
    create_whatsapp_login_token,
    validate_whatsapp_login_token,
)
from apps.accounts.services.whatsapp_identity import find_or_create_whatsapp_identity, link_whatsapp_identity_to_user


class AuthBridgeTests(TestCase):
    def test_protected_pwa_view_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_authenticated_user_can_access_protected_pwa_view(self):
        user = get_user_model().objects.create_user(phone_number="+212700000001", password="x")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_whatsapp_webhook_endpoint_does_not_require_login(self):
        payload = {"entry": []}
        response = self.client.post("/whatsapp/webhook/", data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_whatsapp_identity_created_from_inbound_data(self):
        payload = {
            "entry": [{"changes": [{"value": {"contacts": [{"wa_id": "212611122233", "profile": {"name": "Ali"}}]}}]}]
        }
        self.client.post("/whatsapp/webhook/", data=payload, content_type="application/json")
        identity = WhatsAppIdentity.objects.get(wa_id="212611122233")
        self.assertEqual(identity.display_name, "Ali")

    def test_whatsapp_identity_can_be_linked_to_user(self):
        user = get_user_model().objects.create_user(phone_number="+212700000002", password="x")
        identity = find_or_create_whatsapp_identity("212699998887")
        link_whatsapp_identity_to_user(identity, user)
        identity.refresh_from_db()
        self.assertTrue(identity.is_linked)
        self.assertEqual(identity.user, user)

    @override_settings(SECRET_KEY="test-key")
    def test_magic_login_token_expires(self):
        identity = find_or_create_whatsapp_identity("212600001111")
        token = create_whatsapp_login_token(identity)
        with patch("django.core.signing.time.time", return_value=timezone.now().timestamp() + 700):
            with self.assertRaises(InvalidMagicToken):
                validate_whatsapp_login_token(token)

    def test_magic_login_token_one_time_use(self):
        identity = find_or_create_whatsapp_identity("212600001112")
        token = create_whatsapp_login_token(identity)
        consume_whatsapp_login_token(token)
        with self.assertRaises(InvalidMagicToken):
            consume_whatsapp_login_token(token)

    def test_unsafe_next_url_is_rejected(self):
        identity = find_or_create_whatsapp_identity("212600001113")
        token = create_whatsapp_login_token(identity, next_url="https://evil.com/path")
        payload = validate_whatsapp_login_token(token)
        self.assertIsNone(payload["next_url"])

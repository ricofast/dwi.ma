import logging
import uuid
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class BaseWhatsAppProvider:
    def send_text(self, to, body): raise NotImplementedError
    def send_interactive_buttons(self, to, body, buttons): raise NotImplementedError
    def send_interactive_list(self, to, body, sections): raise NotImplementedError
    def mark_as_read(self, message_id): return None

class MockWhatsAppProvider(BaseWhatsAppProvider):
    sent_payloads = []
    def _fake(self, payload):
        mid = f"mock-{uuid.uuid4()}"
        self.sent_payloads.append({"id": mid, "payload": payload})
        return {"message_id": mid, "status": "sent", "payload": payload}
    def send_text(self, to, body): return self._fake({"to": to, "type": "text", "text": body})
    def send_interactive_buttons(self, to, body, buttons): return self._fake({"to": to, "type": "interactive_buttons", "body": body, "buttons": buttons})
    def send_interactive_list(self, to, body, sections): return self._fake({"to": to, "type": "interactive_list", "body": body, "sections": sections})

class MetaCloudWhatsAppProvider(BaseWhatsAppProvider):
    def __init__(self):
        self.token = getattr(settings, "WHATSAPP_ACCESS_TOKEN", "")
        self.phone_id = getattr(settings, "WHATSAPP_PHONE_NUMBER_ID", "")
        self.api_version = getattr(settings, "WHATSAPP_API_VERSION", "v23.0")
    def _send(self, payload):
        if not self.token or not self.phone_id:
            return {"status": "failed", "error": "missing_credentials"}
        url = f"https://graph.facebook.com/{self.api_version}/{self.phone_id}/messages"
        try:
            r = requests.post(url, json=payload, headers={"Authorization": f"Bearer {self.token}"}, timeout=8)
            data = r.json()
            if r.status_code >= 400:
                logger.warning("WhatsApp provider error: %s", data)
                return {"status": "failed", "error": "provider_error", "response": data}
            msg_id = (((data.get("messages") or [{}])[0]).get("id"))
            return {"status": "sent", "message_id": msg_id, "payload": payload}
        except Exception:
            logger.exception("WhatsApp provider exception")
            return {"status": "failed", "error": "exception"}
    def send_text(self, to, body):
        return self._send({"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": body}})
    def send_interactive_buttons(self, to, body, buttons):
        return self._send({"messaging_product":"whatsapp","to":to,"type":"interactive","interactive":{"type":"button","body":{"text":body},"action":{"buttons":buttons}}})
    def send_interactive_list(self, to, body, sections):
        return self._send({"messaging_product":"whatsapp","to":to,"type":"interactive","interactive":{"type":"list","body":{"text":body},"action":{"button":"اختار","sections":sections}}})

def get_whatsapp_provider():
    provider = getattr(settings, "WHATSAPP_PROVIDER", "mock")
    return MetaCloudWhatsAppProvider() if provider == "meta" else MockWhatsAppProvider()

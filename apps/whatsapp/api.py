import hashlib, hmac, json
from uuid import UUID
from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from pydantic import BaseModel
from apps.accounts.auth import require_auth
from apps.accounts.models import WhatsAppIdentity
from apps.assistant.models import AIJob
from .models import WhatsAppConversationState, WhatsAppOutboundMessage, WhatsAppWebhookEvent
from .services.messages import send_result_message
from .services.providers import get_whatsapp_provider
from .tasks import process_whatsapp_webhook_event

router = Router(tags=["whatsapp"])

@router.get("/whatsapp/webhook")
def verify_webhook(request, hub_mode: str = "", hub_challenge: str = "", hub_verify_token: str = ""):
    token = hub_verify_token or request.GET.get("hub.verify_token", "")
    challenge = hub_challenge or request.GET.get("hub.challenge", "")
    if token and token == getattr(settings, "WHATSAPP_VERIFY_TOKEN", ""):
        return challenge
    raise HttpError(403, "forbidden")

@router.post("/whatsapp/webhook")
def webhook_post(request):
    payload = json.loads(request.body or "{}")
    secret = getattr(settings, "WHATSAPP_APP_SECRET", "")
    if secret:
        sig = request.headers.get("X-Hub-Signature-256", "")
        expected = "sha256=" + hmac.new(secret.encode(), request.body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            raise HttpError(403, "invalid signature")
    event = WhatsAppWebhookEvent.objects.create(event_id=payload.get("object"), payload_json=payload)
    try:
        process_whatsapp_webhook_event.delay(str(event.id))
    except Exception:
        process_whatsapp_webhook_event(str(event.id))
    return {"status": "ok"}

class SendResultIn(BaseModel):
    job_id: UUID
    phone_number: str | None = None

@router.post("/whatsapp/send-result")
def send_result(request, payload: SendResultIn):
    require_auth(request)
    job = get_object_or_404(AIJob, id=payload.job_id, user=request.user)
    if job.status != AIJob.Status.COMPLETED:
        raise HttpError(400, "Job not completed")
    identity = WhatsAppIdentity.objects.filter(user=request.user, is_linked=True).first()
    wa_id = identity.wa_id if identity else payload.phone_number
    if not wa_id: raise HttpError(400, "Link WhatsApp account first")
    text = job.result_text or (job.result_json or {}).get("full_answer_darija") or ""
    resp = send_result_message(wa_id, text)
    WhatsAppOutboundMessage.objects.create(user=request.user, wa_id=wa_id, phone_number=payload.phone_number, message_id=resp.get("message_id"), message_type="text", text_body=text, payload_json=resp, status=resp.get("status", "queued"))
    return {"status": resp.get("status", "queued")}

@router.get('/whatsapp/conversation-state')
def convo_state(request):
    require_auth(request)
    return [{"wa_id":s.wa_id,"current_state":s.current_state} for s in WhatsAppConversationState.objects.filter(user=request.user)]

class TestMessageIn(BaseModel):
    to: str
    body: str

@router.post('/whatsapp/send-test-message')
def send_test(request, payload: TestMessageIn):
    require_auth(request)
    if not request.user.is_staff and not settings.DEBUG:
        raise HttpError(403, "forbidden")
    return get_whatsapp_provider().send_text(payload.to, payload.body)

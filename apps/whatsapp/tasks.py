from celery import shared_task
from django.utils import timezone
from apps.accounts.services.whatsapp_identity import find_or_create_whatsapp_identity, get_user_from_whatsapp_identity
from .models import WhatsAppConversationState, WhatsAppInboundMessage, WhatsAppOutboundMessage, WhatsAppWebhookEvent
from .services.parser import parse_webhook_payload
from .services.router import route_inbound_message

@shared_task
def process_whatsapp_webhook_event(event_id):
    event = WhatsAppWebhookEvent.objects.get(id=event_id)
    try:
        parsed = parse_webhook_payload(event.payload_json)
        for raw in parsed["messages"]:
            identity = find_or_create_whatsapp_identity(raw["wa_id"], raw.get("phone_number"), raw.get("display_name"), raw.get("raw_profile"))
            user = get_user_from_whatsapp_identity(raw["wa_id"])
            inbound, _ = WhatsAppInboundMessage.objects.get_or_create(message_id=raw["message_id"], defaults={**raw, "user": user})
            WhatsAppConversationState.objects.get_or_create(wa_id=raw["wa_id"], defaults={"user": user})
            route_inbound_message(inbound)
        for status in parsed["statuses"]:
            WhatsAppOutboundMessage.objects.filter(message_id=status["message_id"]).update(status=status["status"]) 
        event.processed = True; event.processed_at = timezone.now(); event.processing_error = ""; event.save(update_fields=["processed","processed_at","processing_error"])
    except Exception:
        event.processing_error = "processing_failed"; event.save(update_fields=["processing_error"]); raise

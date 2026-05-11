import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.accounts.services.whatsapp_identity import find_or_create_whatsapp_identity
from .models import WhatsAppWebhookEvent


@csrf_exempt
@require_POST
def webhook(request):
    payload = json.loads(request.body or "{}")
    WhatsAppWebhookEvent.objects.create(payload=payload)

    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            contacts = value.get("contacts", [])
            for contact in contacts:
                profile = contact.get("profile") or {}
                find_or_create_whatsapp_identity(
                    wa_id=contact.get("wa_id"),
                    phone_number=contact.get("wa_id"),
                    display_name=profile.get("name"),
                    raw_profile=contact,
                )
    return JsonResponse({"status": "ok"})

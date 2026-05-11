from django.utils import timezone

from apps.accounts.models import WhatsAppIdentity



def find_or_create_whatsapp_identity(wa_id, phone_number=None, display_name=None, raw_profile=None):
    identity, created = WhatsAppIdentity.objects.get_or_create(
        wa_id=wa_id,
        defaults={
            "phone_number": phone_number,
            "display_name": display_name,
            "raw_profile": raw_profile or {},
            "last_seen_at": timezone.now(),
        },
    )
    if not created:
        changed = False
        identity.last_seen_at = timezone.now()
        if phone_number and identity.phone_number != phone_number:
            identity.phone_number = phone_number
            changed = True
        if display_name and identity.display_name != display_name:
            identity.display_name = display_name
            changed = True
        if raw_profile:
            identity.raw_profile = raw_profile
            changed = True
        identity.save(update_fields=["last_seen_at", "phone_number", "display_name", "raw_profile", "updated_at"])
    return identity


def link_whatsapp_identity_to_user(identity, user):
    identity.user = user
    identity.is_linked = True
    identity.linked_at = identity.linked_at or timezone.now()
    identity.last_seen_at = timezone.now()
    identity.save(update_fields=["user", "is_linked", "linked_at", "last_seen_at", "updated_at"])
    return identity


def get_user_from_whatsapp_identity(wa_id):
    identity = WhatsAppIdentity.objects.filter(wa_id=wa_id, is_linked=True).select_related("user").first()
    return identity.user if identity and identity.user else None

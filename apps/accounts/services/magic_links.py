from django.core import signing
from django.utils.http import url_has_allowed_host_and_scheme

SIGNER_SALT = "accounts.whatsapp.login"
MAX_AGE_SECONDS = 600


class InvalidMagicToken(Exception):
    pass


def _clean_next_url(next_url):
    if not next_url:
        return None
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
        return None
    if not next_url.startswith("/"):
        return None
    return next_url


def create_whatsapp_login_token(wa_identity, action=None, next_url=None):
    payload = {
        "wa_identity_id": str(wa_identity.id),
        "action": action,
        "next_url": _clean_next_url(next_url),
    }
    return signing.dumps(payload, salt=SIGNER_SALT)


def validate_whatsapp_login_token(token):
    try:
        payload = signing.loads(token, salt=SIGNER_SALT, max_age=MAX_AGE_SECONDS)
    except signing.BadSignature as exc:
        raise InvalidMagicToken("Invalid or expired token") from exc
    return payload


def consume_whatsapp_login_token(token):
    payload = validate_whatsapp_login_token(token)
    from apps.accounts.models import WhatsAppIdentity

    identity = WhatsAppIdentity.objects.filter(id=payload["wa_identity_id"]).first()
    if not identity:
        raise InvalidMagicToken("Identity not found")
    if identity.raw_profile.get("last_consumed_token") == token:
        raise InvalidMagicToken("Token already used")
    raw_profile = identity.raw_profile or {}
    raw_profile["last_consumed_token"] = token
    identity.raw_profile = raw_profile
    identity.save(update_fields=["raw_profile", "updated_at"])
    return payload, identity

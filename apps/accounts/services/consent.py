from apps.accounts.models import ConsentLog


def log_consent(user=None, phone_number=None, consent_type=None, accepted=True, source="pwa", request=None, consent_text_version="v1", consent_text_snapshot=""):
    ip = request.META.get("REMOTE_ADDR") if request else None
    ua = request.META.get("HTTP_USER_AGENT") if request else None
    phone = phone_number or (getattr(user, "phone_number", None) if user else None)
    return ConsentLog.objects.create(
        user=user,
        phone_number=phone,
        consent_type=consent_type,
        consent_text_version=consent_text_version,
        consent_text_snapshot=consent_text_snapshot,
        accepted=accepted,
        ip_address=ip,
        user_agent=ua,
        source=source,
    )


def get_latest_consent(user, consent_type):
    return ConsentLog.objects.filter(user=user, consent_type=consent_type).order_by("-created_at").first()


def has_required_consent(user, consent_type):
    c = get_latest_consent(user, consent_type)
    return bool(c and c.accepted)

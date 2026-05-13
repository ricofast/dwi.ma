from apps.core.models import AuditLog


def log_action(actor=None, action="", target=None, metadata=None, request=None):
    return AuditLog.objects.create(
        actor=actor,
        action=action,
        target_type=(target.__class__.__name__ if target else ""),
        target_id=(str(getattr(target, "id", "")) if target else ""),
        metadata_json=metadata or {},
        ip_address=(request.META.get("REMOTE_ADDR") if request else None),
        user_agent=(request.META.get("HTTP_USER_AGENT") if request else None),
    )

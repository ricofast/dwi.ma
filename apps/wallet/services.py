from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import CreditAdjustment, CreditWallet, UsageEvent


def get_wallet(user):
    wallet, _ = CreditWallet.objects.get_or_create(user=user)
    return wallet


def get_balance(user):
    return get_wallet(user).balance


def grant_free_credits(user):
    amount = int(getattr(settings, "DEFAULT_FREE_CREDITS", 3))
    if amount <= 0:
        return get_wallet(user)

    wallet, _ = CreditWallet.objects.get_or_create(user=user)
    if wallet.total_purchased > 0 or wallet.balance > 0:
        return wallet
    add_credits(user=user, amount=amount, reason="signup_free_credits", metadata={"source": "default"})
    return get_wallet(user)


def add_credits(user, amount, reason, metadata=None, created_by=None):
    if amount == 0:
        raise ValidationError("Amount cannot be zero")

    metadata = metadata or {}
    with transaction.atomic():
        wallet = CreditWallet.objects.select_for_update().get(user=user)
        if amount < 0 and wallet.balance < abs(amount):
            raise ValidationError("Insufficient balance for adjustment")

        wallet.balance += amount
        if wallet.balance < 0:
            raise ValidationError("Balance cannot go below zero")

        if amount > 0:
            wallet.total_purchased += amount
        else:
            wallet.total_used += abs(amount)

        wallet.save(update_fields=["balance", "total_purchased", "total_used", "updated_at"])

        CreditAdjustment.objects.create(
            user=user,
            amount=amount,
            reason=reason,
            created_by=created_by,
            metadata=metadata,
        )
    return wallet


def can_spend(user, amount):
    if amount <= 0:
        return True
    return get_balance(user) >= amount


def reserve_credits(user, amount, event_type, reference_type=None, reference_id=None, metadata=None):
    if amount <= 0:
        raise ValidationError("Amount must be positive")
    if not can_spend(user, amount):
        raise ValidationError("Insufficient credits")

    return UsageEvent.objects.create(
        user=user,
        event_type=event_type,
        credits=amount,
        status=UsageEvent.Status.RESERVED,
        reference_type=reference_type or "",
        reference_id=reference_id,
        metadata=metadata or {},
    )


def charge_reserved_usage(usage_event):
    with transaction.atomic():
        usage_event = UsageEvent.objects.select_for_update().select_related("user").get(pk=usage_event.pk)
        if usage_event.status != UsageEvent.Status.RESERVED:
            return usage_event

        wallet = CreditWallet.objects.select_for_update().get(user=usage_event.user)
        if wallet.balance < usage_event.credits:
            raise ValidationError("Insufficient balance")

        wallet.balance -= usage_event.credits
        wallet.total_used += usage_event.credits
        wallet.save(update_fields=["balance", "total_used", "updated_at"])

        usage_event.status = UsageEvent.Status.CHARGED
        usage_event.save(update_fields=["status", "updated_at"])
        return usage_event


def refund_usage(usage_event, reason=None):
    with transaction.atomic():
        usage_event = UsageEvent.objects.select_for_update().select_related("user").get(pk=usage_event.pk)
        if usage_event.status != UsageEvent.Status.CHARGED:
            return usage_event

        wallet = CreditWallet.objects.select_for_update().get(user=usage_event.user)
        wallet.balance += usage_event.credits
        wallet.total_used = max(0, wallet.total_used - usage_event.credits)
        wallet.save(update_fields=["balance", "total_used", "updated_at"])

        usage_event.status = UsageEvent.Status.REFUNDED
        if reason:
            usage_event.metadata = {**usage_event.metadata, "refund_reason": reason}
            usage_event.save(update_fields=["status", "metadata", "updated_at"])
        else:
            usage_event.save(update_fields=["status", "updated_at"])
        return usage_event


def fail_usage(usage_event, reason=None):
    with transaction.atomic():
        usage_event = UsageEvent.objects.select_for_update().get(pk=usage_event.pk)
        if usage_event.status != UsageEvent.Status.RESERVED:
            return usage_event
        usage_event.status = UsageEvent.Status.FAILED
        if reason:
            usage_event.metadata = {**usage_event.metadata, "failure_reason": reason}
            usage_event.save(update_fields=["status", "metadata", "updated_at"])
        else:
            usage_event.save(update_fields=["status", "updated_at"])
        return usage_event

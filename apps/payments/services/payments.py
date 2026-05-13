from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.wallet.models import CreditAdjustment
from apps.wallet.services import add_credits
from apps.payments.models import (
    PaymentCreditGrant,
    PaymentProduct,
    PaymentProvider,
    PaymentTransaction,
    PaymentWebhookEvent,
)
from .providers import generate_idempotency_key, get_provider


def get_active_products():
    return PaymentProduct.objects.filter(active=True).order_by("sort_order", "price_mad")


def create_payment_transaction(user, product_code, provider_code=None):
    product = PaymentProduct.objects.filter(code=product_code, active=True).first()
    if not product:
        raise ValueError("Invalid product_code")
    provider_obj, _ = PaymentProvider.objects.get_or_create(
        code=provider_code or settings.PAYMENT_PROVIDER,
        defaults={"name": (provider_code or settings.PAYMENT_PROVIDER).replace("_", " ").title(), "active": True},
    )
    return PaymentTransaction.objects.create(
        user=user,
        provider=provider_obj,
        product=product,
        amount=product.price_mad,
        currency=product.currency,
        credits_to_add=product.credits,
        idempotency_key=generate_idempotency_key(),
    )


def start_payment(transaction_obj, return_url=None):
    provider = get_provider(transaction_obj.provider.code)
    result = provider.start_payment(transaction_obj, return_url=return_url, callback_url=settings.DIGITAL_VIRGO_CALLBACK_URL)
    transaction_obj.provider_transaction_id = result.provider_transaction_id
    transaction_obj.provider_payment_url = result.payment_url or ""
    transaction_obj.raw_request_json = result.raw_request
    transaction_obj.raw_response_json = result.raw_response
    transaction_obj.status = PaymentTransaction.Status.INITIATED
    transaction_obj.save()
    return transaction_obj


def mark_transaction_paid(transaction_obj, provider_payload=None):
    if transaction_obj.status == PaymentTransaction.Status.PAID:
        return transaction_obj
    transaction_obj.status = PaymentTransaction.Status.PAID
    transaction_obj.paid_at = timezone.now()
    if provider_payload:
        transaction_obj.raw_callback_json = provider_payload
    transaction_obj.save()
    grant_credits_for_paid_transaction(transaction_obj)
    return transaction_obj


def mark_transaction_failed(transaction_obj, reason=None, provider_payload=None, status=PaymentTransaction.Status.FAILED):
    if transaction_obj.status == PaymentTransaction.Status.PAID:
        return transaction_obj
    transaction_obj.status = status
    transaction_obj.failure_reason = reason or ""
    if provider_payload:
        transaction_obj.raw_callback_json = provider_payload
    transaction_obj.save()
    return transaction_obj


def grant_credits_for_paid_transaction(transaction_obj):
    grant = PaymentCreditGrant.objects.filter(transaction=transaction_obj).first()
    if grant:
        return grant
    wallet_before = CreditAdjustment.objects.filter(user=transaction_obj.user).order_by("-created_at").first()
    add_credits(
        user=transaction_obj.user,
        amount=transaction_obj.credits_to_add,
        reason="payment_credit_purchase",
        metadata={"payment_transaction_id": str(transaction_obj.id), "provider": transaction_obj.provider.code},
    )
    wallet_adj = CreditAdjustment.objects.filter(user=transaction_obj.user).exclude(pk=getattr(wallet_before, "pk", None)).order_by("-created_at").first()
    return PaymentCreditGrant.objects.create(
        transaction=transaction_obj,
        user=transaction_obj.user,
        credits_granted=transaction_obj.credits_to_add,
        wallet_adjustment=wallet_adj,
    )


def handle_payment_callback(provider_code, payload, headers=None):
    provider = get_provider(provider_code)
    parsed = provider.parse_callback(payload)
    signature_valid = provider.verify_callback(payload, headers=headers)
    event = PaymentWebhookEvent.objects.create(
        provider_code=provider_code,
        provider_transaction_id=parsed.get("provider_transaction_id"),
        payload_json=payload,
        signature_valid=signature_valid,
    )
    if not signature_valid:
        event.processing_error = "invalid_signature"
        event.save(update_fields=["processing_error"])
        return event

    provider_tx = parsed.get("provider_transaction_id")
    with transaction.atomic():
        tx = PaymentTransaction.objects.select_for_update().filter(provider=PaymentProvider.objects.get(code=provider_code), provider_transaction_id=provider_tx).first()
        if not tx:
            event.processing_error = "unknown_transaction"
            event.save(update_fields=["processing_error"])
            return event
        normalized_status = parsed.get("status")
        tx.provider_status = parsed.get("provider_status") or ""
        tx.raw_callback_json = payload
        tx.save(update_fields=["provider_status", "raw_callback_json", "updated_at"])
        if normalized_status == "paid":
            mark_transaction_paid(tx, provider_payload=payload)
        elif normalized_status == "failed":
            mark_transaction_failed(tx, reason="provider_failed", provider_payload=payload)
        elif normalized_status == "cancelled":
            mark_transaction_failed(tx, reason="provider_cancelled", provider_payload=payload, status=PaymentTransaction.Status.CANCELLED)
        elif normalized_status == "expired":
            mark_transaction_failed(tx, reason="provider_expired", provider_payload=payload, status=PaymentTransaction.Status.EXPIRED)
    event.processed = True
    event.processed_at = timezone.now()
    event.save(update_fields=["processed", "processed_at"])
    return event


def expire_old_pending_transactions():
    cutoff = timezone.now() - timedelta(minutes=settings.PAYMENT_TRANSACTION_EXPIRY_MINUTES)
    return PaymentTransaction.objects.filter(status__in=[PaymentTransaction.Status.PENDING, PaymentTransaction.Status.INITIATED], created_at__lt=cutoff).update(status=PaymentTransaction.Status.EXPIRED)


def get_user_transactions(user):
    return PaymentTransaction.objects.filter(user=user).order_by("-created_at")

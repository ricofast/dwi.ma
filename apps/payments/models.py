import uuid

from django.conf import settings
from django.db import models


class PaymentProvider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
    config = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class PaymentProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    price_mad = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default="MAD")
    credits = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "price_mad", "created_at"]


class PaymentTransaction(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        INITIATED = "initiated", "Initiated"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"
        REFUNDED = "refunded", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payment_transactions")
    provider = models.ForeignKey(PaymentProvider, on_delete=models.PROTECT, related_name="transactions")
    product = models.ForeignKey(PaymentProduct, on_delete=models.PROTECT, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default="MAD")
    credits_to_add = models.PositiveIntegerField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    provider_transaction_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    provider_payment_url = models.URLField(blank=True)
    provider_status = models.CharField(max_length=64, blank=True)
    idempotency_key = models.CharField(max_length=128, unique=True)
    raw_request_json = models.JSONField(default=dict, blank=True)
    raw_response_json = models.JSONField(default=dict, blank=True)
    raw_callback_json = models.JSONField(default=dict, blank=True)
    failure_reason = models.TextField(blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "status", "created_at"]),
            models.Index(fields=["provider", "status", "created_at"]),
        ]


class PaymentWebhookEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider_code = models.CharField(max_length=64)
    event_id = models.CharField(max_length=255, null=True, blank=True)
    provider_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    payload_json = models.JSONField(default=dict)
    signature_valid = models.BooleanField(null=True, blank=True)
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)


class PaymentCreditGrant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.OneToOneField(PaymentTransaction, on_delete=models.PROTECT, related_name="credit_grant")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payment_credit_grants")
    credits_granted = models.PositiveIntegerField()
    wallet_adjustment = models.ForeignKey(
        "wallet.CreditAdjustment", null=True, blank=True, on_delete=models.SET_NULL, related_name="payment_credit_grants"
    )
    created_at = models.DateTimeField(auto_now_add=True)

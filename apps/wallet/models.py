import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class CreditWallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="credit_wallet")
    balance = models.PositiveIntegerField(default=0)
    total_purchased = models.PositiveIntegerField(default=0)
    total_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Wallet<{self.user}>: {self.balance}"


class UsageEvent(models.Model):
    class Status(models.TextChoices):
        RESERVED = "reserved", "Reserved"
        CHARGED = "charged", "Charged"
        REFUNDED = "refunded", "Refunded"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="usage_events")
    event_type = models.CharField(max_length=64)
    credits = models.PositiveIntegerField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.RESERVED)
    reference_type = models.CharField(max_length=64, blank=True)
    reference_id = models.UUIDField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "status", "created_at"]),
            models.Index(fields=["event_type", "created_at"]),
        ]


class CreditAdjustment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="credit_adjustments")
    amount = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_credit_adjustments",
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
        ]

    def clean(self):
        if self.amount == 0:
            raise ValidationError("Adjustment amount cannot be zero.")

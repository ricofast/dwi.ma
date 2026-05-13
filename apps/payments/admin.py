from django.conf import settings
from django.contrib import admin, messages

from apps.payments.models import PaymentCreditGrant, PaymentProduct, PaymentProvider, PaymentTransaction, PaymentWebhookEvent
from apps.payments.services.payments import handle_payment_callback, mark_transaction_paid


@admin.register(PaymentProvider)
class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "active", "created_at")


@admin.register(PaymentProduct)
class PaymentProductAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "price_mad", "currency", "credits", "active", "sort_order")
    list_filter = ("active", "currency")


@admin.action(description="Mark selected pending as paid (testing)")
def mark_pending_paid(modeladmin, request, queryset):
    if not settings.DEBUG:
        messages.error(request, "Only allowed in DEBUG")
        return
    for tx in queryset.filter(status__in=[PaymentTransaction.Status.PENDING, PaymentTransaction.Status.INITIATED]):
        mark_transaction_paid(tx, provider_payload={"admin": True})


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "provider", "product", "amount", "currency", "credits_to_add", "status", "provider_transaction_id", "created_at", "paid_at")
    list_filter = ("provider", "product", "status", "currency", "created_at", "paid_at")
    actions = [mark_pending_paid]


@admin.action(description="Retry processing webhook event")
def retry_webhook(modeladmin, request, queryset):
    for event in queryset:
        handle_payment_callback(event.provider_code, event.payload_json)


@admin.register(PaymentWebhookEvent)
class PaymentWebhookEventAdmin(admin.ModelAdmin):
    list_display = ("provider_code", "event_id", "provider_transaction_id", "signature_valid", "processed", "received_at", "processed_at")
    list_filter = ("provider_code", "signature_valid", "processed", "received_at")
    actions = [retry_webhook]


@admin.register(PaymentCreditGrant)
class PaymentCreditGrantAdmin(admin.ModelAdmin):
    list_display = ("transaction", "user", "credits_granted", "wallet_adjustment", "created_at")

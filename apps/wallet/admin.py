from django.contrib import admin

from .models import CreditAdjustment, CreditWallet, UsageEvent


@admin.register(CreditWallet)
class CreditWalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "total_purchased", "total_used", "created_at", "updated_at")
    search_fields = ("user__phone_number", "user__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(UsageEvent)
class UsageEventAdmin(admin.ModelAdmin):
    list_display = ("user", "event_type", "credits", "status", "created_at", "updated_at")
    list_filter = ("status", "event_type")
    search_fields = ("user__phone_number", "reference_type")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CreditAdjustment)
class CreditAdjustmentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "reason", "created_by", "created_at")
    search_fields = ("user__phone_number", "reason")
    readonly_fields = ("created_at",)

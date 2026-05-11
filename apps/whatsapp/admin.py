from django.contrib import admin
from .models import WhatsAppConversationState, WhatsAppInboundMessage, WhatsAppOutboundMessage, WhatsAppWebhookEvent

@admin.register(WhatsAppWebhookEvent)
class WhatsAppWebhookEventAdmin(admin.ModelAdmin):
    list_display = ("id","event_id","processed","received_at","processed_at")
    list_filter = ("processed","received_at")

@admin.register(WhatsAppInboundMessage)
class WhatsAppInboundMessageAdmin(admin.ModelAdmin):
    list_display = ("wa_id","user","message_type","created_at")
    list_filter = ("message_type","created_at")

@admin.register(WhatsAppOutboundMessage)
class WhatsAppOutboundMessageAdmin(admin.ModelAdmin):
    list_display = ("wa_id","user","message_type","status","created_at","updated_at")
    list_filter = ("message_type","status","created_at")

@admin.register(WhatsAppConversationState)
class WhatsAppConversationStateAdmin(admin.ModelAdmin):
    list_display = ("wa_id","user","current_state","created_at","updated_at")
    list_filter = ("current_state","created_at")

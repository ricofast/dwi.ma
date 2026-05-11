import uuid

from django.conf import settings
from django.db import models


class WhatsAppWebhookEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.CharField(max_length=255, null=True, blank=True)
    payload_json = models.JSONField(default=dict)
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)


class WhatsAppInboundMessage(models.Model):
    class MessageType(models.TextChoices):
        TEXT = "text", "Text"
        AUDIO = "audio", "Audio"
        IMAGE = "image", "Image"
        DOCUMENT = "document", "Document"
        INTERACTIVE = "interactive", "Interactive"
        BUTTON = "button", "Button"
        LIST_REPLY = "list_reply", "List Reply"
        UNKNOWN = "unknown", "Unknown"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="wa_inbound_messages")
    wa_id = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    message_id = models.CharField(max_length=255, unique=True)
    message_type = models.CharField(max_length=20, choices=MessageType.choices, default=MessageType.UNKNOWN)
    text_body = models.TextField(null=True, blank=True)
    media_id = models.CharField(max_length=255, null=True, blank=True)
    interactive_payload = models.JSONField(null=True, blank=True)
    raw_payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class WhatsAppOutboundMessage(models.Model):
    class MessageType(models.TextChoices):
        TEXT = "text", "Text"
        INTERACTIVE_BUTTONS = "interactive_buttons", "Interactive Buttons"
        INTERACTIVE_LIST = "interactive_list", "Interactive List"
        TEMPLATE = "template", "Template"
        DOCUMENT = "document", "Document"
        UNKNOWN = "unknown", "Unknown"

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        SENT = "sent", "Sent"
        DELIVERED = "delivered", "Delivered"
        READ = "read", "Read"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="wa_outbound_messages")
    wa_id = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    message_id = models.CharField(max_length=255, null=True, blank=True)
    message_type = models.CharField(max_length=32, choices=MessageType.choices, default=MessageType.TEXT)
    text_body = models.TextField(null=True, blank=True)
    payload_json = models.JSONField(default=dict)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.QUEUED)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WhatsAppConversationState(models.Model):
    class State(models.TextChoices):
        MAIN_MENU = "main_menu", "Main Menu"
        WAITING_FOR_TEXT = "waiting_for_text", "Waiting for text"
        WAITING_FOR_DOCUMENT = "waiting_for_document", "Waiting for document"
        WAITING_FOR_ACTION = "waiting_for_action", "Waiting for action"
        LINKED = "linked", "Linked"
        UNKNOWN = "unknown", "Unknown"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="wa_conversation_states")
    wa_id = models.CharField(max_length=64, unique=True)
    current_state = models.CharField(max_length=32, choices=State.choices, default=State.UNKNOWN)
    context = models.JSONField(default=dict, blank=True)
    last_seen_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

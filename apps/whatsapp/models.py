import uuid

from django.db import models


class WhatsAppWebhookEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

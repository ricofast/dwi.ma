import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone_number: str, password: str | None = None, **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.phone_number


class Profile(models.Model):
    class PreferredLanguage(models.TextChoices):
        DARIJA_ARABIC = "darija_arabic", "Darija (Arabic script)"
        DARIJA_LATIN = "darija_latin", "Darija (Latin script)"
        FRENCH = "french", "French"
        ARABIC = "arabic", "Arabic"

    class PreferredOutputChannel(models.TextChoices):
        WEB = "web", "Web"
        WHATSAPP = "whatsapp", "WhatsApp"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    preferred_language = models.CharField(max_length=32, choices=PreferredLanguage.choices, default=PreferredLanguage.DARIJA_ARABIC)
    preferred_output_channel = models.CharField(max_length=16, choices=PreferredOutputChannel.choices, default=PreferredOutputChannel.WEB)
    whatsapp_opt_in = models.BooleanField(default=False)
    onboarding_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PhoneIdentity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="phone_identities")
    phone_number = models.CharField(max_length=20, unique=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class WhatsAppIdentity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="whatsapp_identities")
    wa_id = models.CharField(max_length=64, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    is_linked = models.BooleanField(default=False)
    linked_at = models.DateTimeField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    raw_profile = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["created_at"]),
        ]


class ConsentLog(models.Model):
    class ConsentType(models.TextChoices):
        PRIVACY_POLICY = "privacy_policy", "Privacy Policy"
        DOCUMENT_PROCESSING = "document_processing", "Document Processing"
        AUDIO_PROCESSING = "audio_processing", "Audio Processing"
        WHATSAPP_OPTIN = "whatsapp_optin", "WhatsApp Opt-in"
        PAYMENT_TERMS = "payment_terms", "Payment Terms"
        MARKETING = "marketing", "Marketing"

    class Source(models.TextChoices):
        PWA = "pwa", "PWA"
        WHATSAPP = "whatsapp", "WhatsApp"
        ADMIN = "admin", "Admin"
        API = "api", "API"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="consent_logs")
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    consent_type = models.CharField(max_length=32, choices=ConsentType.choices)
    consent_text_version = models.CharField(max_length=32, default="v1")
    consent_text_snapshot = models.TextField(blank=True, default="")
    accepted = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=16, choices=Source.choices, default=Source.PWA)
    created_at = models.DateTimeField(auto_now_add=True)

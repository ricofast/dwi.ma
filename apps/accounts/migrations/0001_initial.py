import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False)),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("phone_number", models.CharField(max_length=20, unique=True)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("full_name", models.CharField(blank=True, max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("groups", models.ManyToManyField(blank=True, related_name="user_set", related_query_name="user", to="auth.group")),
                ("user_permissions", models.ManyToManyField(blank=True, related_name="user_set", related_query_name="user", to="auth.permission")),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("preferred_language", models.CharField(choices=[("darija_arabic", "Darija (Arabic script)"), ("darija_latin", "Darija (Latin script)"), ("french", "French"), ("arabic", "Arabic")], default="darija_arabic", max_length=32)),
                ("preferred_output_channel", models.CharField(choices=[("web", "Web"), ("whatsapp", "WhatsApp")], default="web", max_length=16)),
                ("whatsapp_opt_in", models.BooleanField(default=False)),
                ("onboarding_completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="accounts.user")),
            ],
        ),
        migrations.CreateModel(
            name="PhoneIdentity",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("phone_number", models.CharField(max_length=20, unique=True)),
                ("is_verified", models.BooleanField(default=False)),
                ("verified_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="phone_identities", to="accounts.user")),
            ],
        ),
        migrations.CreateModel(
            name="WhatsAppIdentity",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("wa_id", models.CharField(max_length=64, unique=True)),
                ("phone_number", models.CharField(blank=True, max_length=20, null=True)),
                ("display_name", models.CharField(blank=True, max_length=255, null=True)),
                ("is_linked", models.BooleanField(default=False)),
                ("linked_at", models.DateTimeField(blank=True, null=True)),
                ("last_seen_at", models.DateTimeField(blank=True, null=True)),
                ("raw_profile", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="whatsapp_identities", to="accounts.user")),
            ],
            options={"indexes": [models.Index(fields=["user"], name="accounts_wh_user_id_9ad6c0_idx"), models.Index(fields=["created_at"], name="accounts_wh_created_bddf02_idx")]},
        ),
    ]

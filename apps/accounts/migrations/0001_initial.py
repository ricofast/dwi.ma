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
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("phone_number", models.CharField(max_length=20, unique=True)),
                ("email", models.EmailField(max_length=254, blank=True)),
                ("full_name", models.CharField(max_length=255, blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("is_superuser", models.BooleanField(default=False)),
                ("groups", models.ManyToManyField(blank=True, related_name="accounts_user_set", related_query_name="accounts_user", to="auth.group")),
                ("user_permissions", models.ManyToManyField(blank=True, related_name="accounts_user_set", related_query_name="accounts_user", to="auth.permission")),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("preferred_language", models.CharField(max_length=32, default="darija_arabic", choices=[("darija_arabic", "Darija (Arabic script)"), ("darija_latin", "Darija (Latin script)"), ("french", "French"), ("arabic", "Arabic")])),
                ("preferred_output_channel", models.CharField(max_length=16, default="web", choices=[("web", "Web"), ("whatsapp", "WhatsApp")])),
                ("whatsapp_opt_in", models.BooleanField(default=False)),
                ("onboarding_completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=models.CASCADE, related_name="profile", to="accounts.user")),
            ],
        ),
    ]

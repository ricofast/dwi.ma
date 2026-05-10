import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CreditWallet",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("balance", models.PositiveIntegerField(default=0)),
                ("total_purchased", models.PositiveIntegerField(default=0)),
                ("total_used", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="credit_wallet", to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CreditAdjustment",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("amount", models.IntegerField()),
                ("reason", models.CharField(max_length=255)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_credit_adjustments", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="credit_adjustments", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"indexes": [models.Index(fields=["user", "created_at"], name="wallet_credi_user_id_3e2e14_idx")]},
        ),
        migrations.CreateModel(
            name="UsageEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("event_type", models.CharField(max_length=64)),
                ("credits", models.PositiveIntegerField()),
                ("status", models.CharField(choices=[("reserved", "Reserved"), ("charged", "Charged"), ("refunded", "Refunded"), ("failed", "Failed")], default="reserved", max_length=16)),
                ("reference_type", models.CharField(blank=True, max_length=64)),
                ("reference_id", models.UUIDField(blank=True, null=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="usage_events", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["user", "status", "created_at"], name="wallet_usage_user_id_0d7edf_idx"),
                    models.Index(fields=["event_type", "created_at"], name="wallet_usage_event_t_b5b0ee_idx"),
                ]
            },
        ),
    ]

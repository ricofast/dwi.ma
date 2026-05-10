from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase, override_settings

from apps.wallet.models import CreditAdjustment, UsageEvent
from apps.wallet.services import (
    add_credits,
    can_spend,
    charge_reserved_usage,
    fail_usage,
    get_wallet,
    refund_usage,
    reserve_credits,
)


@override_settings(DEFAULT_FREE_CREDITS=3)
class WalletTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(phone_number="+212600000100", password="secret")

    def test_wallet_created_automatically_for_new_user(self):
        wallet = get_wallet(self.user)
        self.assertIsNotNone(wallet)

    def test_new_user_receives_default_free_credits(self):
        wallet = get_wallet(self.user)
        self.assertEqual(wallet.balance, 3)

    def test_can_spend_true_when_enough(self):
        self.assertTrue(can_spend(self.user, 2))

    def test_can_spend_false_when_insufficient(self):
        self.assertFalse(can_spend(self.user, 10))

    def test_reserve_credits_creates_reserved_usage_event(self):
        event = reserve_credits(self.user, 2, "document_explanation")
        self.assertEqual(event.status, UsageEvent.Status.RESERVED)

    def test_charge_reserved_usage_deducts_credits(self):
        event = reserve_credits(self.user, 2, "document_explanation")
        charge_reserved_usage(event)
        self.assertEqual(get_wallet(self.user).balance, 1)

    def test_fail_usage_does_not_deduct_credits(self):
        event = reserve_credits(self.user, 2, "document_explanation")
        fail_usage(event, reason="job failed")
        self.assertEqual(get_wallet(self.user).balance, 3)

    def test_refund_usage_restores_credits_after_charge(self):
        event = reserve_credits(self.user, 2, "document_explanation")
        charge_reserved_usage(event)
        refund_usage(event)
        self.assertEqual(get_wallet(self.user).balance, 3)

    def test_duplicate_charging_prevented(self):
        event = reserve_credits(self.user, 2, "document_explanation")
        charge_reserved_usage(event)
        charge_reserved_usage(event)
        self.assertEqual(get_wallet(self.user).balance, 1)

    def test_balance_cannot_go_below_zero(self):
        with self.assertRaises(ValidationError):
            add_credits(self.user, -100, "bad_adjust")

    def test_staff_adjustment_can_add_credits(self):
        staff = get_user_model().objects.create_user(phone_number="+212600000101", password="secret", is_staff=True)
        client = Client()
        client.force_login(staff)
        response = client.post(
            "/api/wallet/admin-adjust/",
            data={"user_id": str(self.user.id), "amount": 5, "reason": "support_add", "metadata": {"ticket": "1"}},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_wallet(self.user).balance, 8)

    def test_staff_adjustment_remove_requires_sufficient_balance(self):
        staff = get_user_model().objects.create_user(phone_number="+212600000102", password="secret", is_staff=True)
        client = Client()
        client.force_login(staff)
        response = client.post(
            "/api/wallet/admin-adjust/",
            data={"user_id": str(self.user.id), "amount": -20, "reason": "support_remove"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CreditAdjustment.objects.filter(user=self.user).count(), 1)

import pytest
from django.core.management import call_command

from apps.payments.models import PaymentCreditGrant, PaymentProduct, PaymentTransaction, PaymentWebhookEvent


@pytest.mark.django_db
def test_seed_products_idempotent():
    call_command("seed_payment_products")
    call_command("seed_payment_products")
    assert PaymentProduct.objects.filter(code="MINI_10").count() == 1


@pytest.mark.django_db
def test_products_endpoint_active_only(client):
    PaymentProduct.objects.create(code="X", name="x", price_mad="1.00", credits=1, active=False)
    call_command("seed_payment_products")
    resp = client.get("/api/payments/products")
    assert resp.status_code == 200
    assert all(p["code"] != "X" for p in resp.json()["products"])


@pytest.mark.django_db
def test_start_payment_and_callback_flow(client, django_user_model):
    user = django_user_model.objects.create_user(phone_number="+212600000001", password="x")
    call_command("seed_payment_products")
    client.force_login(user)
    resp = client.post("/api/payments/start", data={"product_code": "MINI_10"}, content_type="application/json")
    assert resp.status_code == 200
    tx_id = resp.json()["transaction_id"]
    tx = PaymentTransaction.objects.get(id=tx_id)
    assert tx.amount == tx.product.price_mad
    assert tx.credits_to_add == tx.product.credits
    cb = client.post("/api/payments/mock/callback", data={"provider_transaction_id": tx.provider_transaction_id, "status": "PAID"}, content_type="application/json")
    assert cb.status_code == 200
    tx.refresh_from_db()
    assert tx.status == PaymentTransaction.Status.PAID
    assert PaymentCreditGrant.objects.filter(transaction=tx).count() == 1
    cb2 = client.post("/api/payments/mock/callback", data={"provider_transaction_id": tx.provider_transaction_id, "status": "PAID"}, content_type="application/json")
    assert cb2.status_code == 200
    assert PaymentCreditGrant.objects.filter(transaction=tx).count() == 1


@pytest.mark.django_db
def test_security_transaction_isolation(client, django_user_model):
    u1 = django_user_model.objects.create_user(phone_number="+212600000002", password="x")
    u2 = django_user_model.objects.create_user(phone_number="+212600000003", password="x")
    call_command("seed_payment_products")
    client.force_login(u1)
    tx = PaymentTransaction.objects.create(user=u1, provider_id=None, product=PaymentProduct.objects.first(), amount="1.00", credits_to_add=1, currency="MAD", idempotency_key="abc")
    client.force_login(u2)
    resp = client.get(f"/api/payments/transactions/{tx.id}")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_webhook_event_stored_on_unknown(client):
    resp = client.post("/api/payments/mock/callback", data={"provider_transaction_id": "unknown", "status": "UNKNOWN"}, content_type="application/json")
    assert resp.status_code == 200
    assert PaymentWebhookEvent.objects.count() == 1

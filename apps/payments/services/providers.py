import hashlib
import hmac
import uuid
from dataclasses import dataclass

from django.conf import settings


@dataclass
class ProviderStartResult:
    provider_transaction_id: str | None
    payment_url: str | None
    raw_request: dict
    raw_response: dict


class BasePaymentProvider:
    code = "base"

    def start_payment(self, transaction, return_url=None, callback_url=None):
        raise NotImplementedError

    def verify_callback(self, payload, headers=None):
        return True

    def parse_callback(self, payload):
        raise NotImplementedError

    def refund(self, transaction, amount=None, reason=None):
        return {"ok": False, "reason": "refund_not_implemented"}


class MockPaymentProvider(BasePaymentProvider):
    code = "mock"

    def start_payment(self, transaction, return_url=None, callback_url=None):
        pid = f"mock-{transaction.id}"
        status = "success"
        url = f"https://mock-pay.local/pay/{transaction.id}?result={status}"
        return ProviderStartResult(pid, url, {"mock": True}, {"payment_url": url, "transaction_id": pid})

    def parse_callback(self, payload):
        provider_status = payload.get("status") or payload.get("provider_status") or "PENDING"
        return {
            "provider_transaction_id": payload.get("provider_transaction_id"),
            "status": normalize_provider_status(provider_status),
            "amount": payload.get("amount"),
            "currency": payload.get("currency", "MAD"),
            "product_code": payload.get("product_code"),
            "phone_number": payload.get("phone_number"),
            "raw": payload,
            "provider_status": provider_status,
        }


class DigitalVirgoProvider(BasePaymentProvider):
    code = "digital_virgo"

    def _has_credentials(self):
        return bool(settings.DIGITAL_VIRGO_API_BASE_URL and settings.DIGITAL_VIRGO_MERCHANT_ID and settings.DIGITAL_VIRGO_API_KEY)

    def start_payment(self, transaction, return_url=None, callback_url=None):
        request_payload = {
            "merchant_id": settings.DIGITAL_VIRGO_MERCHANT_ID,
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "reference": str(transaction.id),
            "product_code": transaction.product.code,
            "return_url": return_url or settings.DIGITAL_VIRGO_RETURN_URL,
            "callback_url": callback_url or settings.DIGITAL_VIRGO_CALLBACK_URL,
        }
        if not self._has_credentials():
            return ProviderStartResult(None, None, request_payload, {"error": "missing_digital_virgo_credentials"})
        # TODO: Replace this placeholder with real merchant-specific Digital Virgo API call/fields.
        provider_tx = f"dv-placeholder-{transaction.id}"
        payment_url = f"{settings.DIGITAL_VIRGO_API_BASE_URL.rstrip('/')}/pay/{provider_tx}"
        return ProviderStartResult(provider_tx, payment_url, request_payload, {"placeholder": True, "payment_url": payment_url})

    def verify_callback(self, payload, headers=None):
        secret = settings.DIGITAL_VIRGO_WEBHOOK_SECRET
        if not secret:
            return True
        signature = (headers or {}).get("X-DV-Signature", "")
        body = str(payload).encode("utf-8")
        expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected)

    def parse_callback(self, payload):
        # TODO: Map final Digital Virgo production field names from merchant docs.
        provider_status = payload.get("status") or payload.get("payment_status") or payload.get("state") or "UNKNOWN"
        return {
            "provider_transaction_id": payload.get("provider_transaction_id") or payload.get("transaction_id") or payload.get("id"),
            "status": normalize_provider_status(provider_status),
            "amount": payload.get("amount"),
            "currency": payload.get("currency", "MAD"),
            "product_code": payload.get("product_code"),
            "phone_number": payload.get("phone_number") or payload.get("msisdn"),
            "raw": payload,
            "provider_status": provider_status,
        }


def normalize_provider_status(provider_status: str):
    status = (provider_status or "").upper()
    if status in {"SUCCESS", "PAID", "CONFIRMED"}:
        return "paid"
    if status in {"FAILED", "ERROR", "DECLINED"}:
        return "failed"
    if status in {"CANCELLED", "CANCELED"}:
        return "cancelled"
    if status in {"EXPIRED", "TIMEOUT"}:
        return "expired"
    if status in {"PENDING", "INITIATED"}:
        return "pending"
    return "unknown"


def get_provider(provider_code=None):
    code = provider_code or settings.PAYMENT_PROVIDER
    if code == "digital_virgo":
        return DigitalVirgoProvider()
    return MockPaymentProvider()


def generate_idempotency_key():
    return uuid.uuid4().hex

from uuid import UUID

from django.conf import settings
from ninja import Router, Schema

from apps.accounts.auth import require_auth
from apps.payments.models import PaymentTransaction
from apps.payments.services.payments import (
    create_payment_transaction,
    get_active_products,
    get_user_transactions,
    handle_payment_callback,
    start_payment,
)

router = Router(tags=["payments"])


class StartIn(Schema):
    product_code: str
    consent_accepted: bool = False


@router.get("/payments/products")
def products(request):
    return {
        "products": [
            {
                "code": p.code,
                "name": p.name,
                "price_mad": str(p.price_mad),
                "currency": p.currency,
                "credits": p.credits,
                "description": p.description,
            }
            for p in get_active_products()
        ]
    }


@router.post("/payments/start")
def start(request, payload: StartIn):
    user = require_auth(request)
    if not payload.consent_accepted:
        return 400, {"detail": "خاصك توافق على شروط الأداء"}
    from apps.accounts.services.consent import log_consent
    from apps.accounts.models import ConsentLog

    log_consent(user=user, consent_type=ConsentLog.ConsentType.PAYMENT_TERMS, accepted=True, source="api", request=request, consent_text_snapshot="كنوافق على شروط الأداء واستعمال الكريديات.")
    try:
        tx = create_payment_transaction(user, payload.product_code)
    except ValueError as exc:
        return 400, {"detail": str(exc)}
    tx = start_payment(tx)
    return {"transaction_id": str(tx.id), "status": tx.status, "payment_url": tx.provider_payment_url or None}


@router.get("/payments/transactions")
def transactions(request):
    user = require_auth(request)
    return [
        {
            "transaction_id": str(t.id),
            "status": t.status,
            "amount": str(t.amount),
            "credits": t.credits_to_add,
            "created_at": t.created_at.isoformat(),
        }
        for t in get_user_transactions(user)[:50]
    ]


@router.get("/payments/transactions/{transaction_id}")
def transaction_detail(request, transaction_id: UUID):
    user = require_auth(request)
    t = PaymentTransaction.objects.filter(id=transaction_id, user=user).first()
    if not t:
        return 404, {"detail": "Not found"}
    return {"transaction_id": str(t.id), "status": t.status, "payment_url": t.provider_payment_url or None}


@router.post("/payments/digital-virgo/callback")
def digital_virgo_callback(request, payload: dict):
    event = handle_payment_callback("digital_virgo", payload, headers=request.headers)
    return 200, {"ok": True, "event_id": str(event.id), "processed": event.processed}


@router.post("/payments/mock/callback")
def mock_callback(request, payload: dict):
    if not (settings.DEBUG or settings.PAYMENT_PROVIDER == "mock"):
        return 404, {"detail": "Not found"}
    event = handle_payment_callback("mock", payload, headers=request.headers)
    return 200, {"ok": True, "event_id": str(event.id), "processed": event.processed}

from django.core.exceptions import ValidationError
from ninja import Router, Schema

from .models import UsageEvent
from .services import add_credits, get_wallet

router = Router(tags=["wallet"])


class WalletResponse(Schema):
    balance: int
    total_purchased: int
    total_used: int


class UsageEventResponse(Schema):
    id: str
    event_type: str
    credits: int
    status: str
    reference_type: str | None = None
    reference_id: str | None = None
    metadata: dict
    created_at: str
    updated_at: str


class AdminAdjustIn(Schema):
    user_id: str
    amount: int
    reason: str
    metadata: dict | None = None


@router.get("/wallet/", response=WalletResponse)
def wallet_detail(request):
    if not request.user.is_authenticated:
        return 401, {"detail": "Authentication required"}
    wallet = get_wallet(request.user)
    return WalletResponse(
        balance=wallet.balance,
        total_purchased=wallet.total_purchased,
        total_used=wallet.total_used,
    )


@router.get("/wallet/usage/", response=list[UsageEventResponse])
def wallet_usage(request):
    if not request.user.is_authenticated:
        return 401, {"detail": "Authentication required"}
    events = UsageEvent.objects.filter(user=request.user).order_by("-created_at")[:50]
    return [
        UsageEventResponse(
            id=str(event.id),
            event_type=event.event_type,
            credits=event.credits,
            status=event.status,
            reference_type=event.reference_type or None,
            reference_id=str(event.reference_id) if event.reference_id else None,
            metadata=event.metadata,
            created_at=event.created_at.isoformat(),
            updated_at=event.updated_at.isoformat(),
        )
        for event in events
    ]


@router.post("/wallet/admin-adjust/")
def wallet_admin_adjust(request, payload: AdminAdjustIn):
    if not request.user.is_authenticated:
        return 401, {"detail": "Authentication required"}
    if not request.user.is_staff:
        return 403, {"detail": "Staff only"}

    from django.contrib.auth import get_user_model

    user = get_user_model().objects.get(pk=payload.user_id)
    try:
        wallet = add_credits(
            user=user,
            amount=payload.amount,
            reason=payload.reason,
            metadata=payload.metadata,
            created_by=request.user,
        )
    except ValidationError as exc:
        return 400, {"detail": exc.message}

    return {"user_id": str(user.id), "balance": wallet.balance}

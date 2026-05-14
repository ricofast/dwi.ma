from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.wallet.models import UsageEvent
from apps.wallet.services import get_wallet


class WalletBalanceView(LoginRequiredMixin, TemplateView):
    template_name = "wallet/balance.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = get_wallet(user)
        ctx["wallet"] = wallet
        ctx["active_tab"] = "wallet"
        ctx["recent_usage"] = (
            UsageEvent.objects.filter(user=user)
            .order_by("-created_at")[:10]
        )
        return ctx

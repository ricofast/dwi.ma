from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.assistant.models import AIJob
from apps.wallet.services import get_wallet


def landing(request):
    return render(request, "landing.html")


def privacy_policy(request):
    return render(request, "legal/privacy.html")


def terms_of_service(request):
    return render(request, "legal/terms.html")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = get_wallet(user)
        ctx["wallet"] = wallet
        ctx["recent_jobs"] = (
            AIJob.objects.filter(user=user)
            .order_by("-created_at")[:5]
        )
        ctx["active_tab"] = "home"
        return ctx

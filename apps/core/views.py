from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
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


def offline(request):
    return render(request, "offline.html")


def service_worker(request):
    sw_path = settings.BASE_DIR / "staticfiles" / "sw.js"
    with open(sw_path, "r", encoding="utf-8") as f:
        return HttpResponse(f.read(), content_type="application/javascript")


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

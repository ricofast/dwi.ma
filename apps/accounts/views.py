from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from apps.accounts.forms import PhoneLoginForm, PhoneRegisterForm
from apps.accounts.models import Profile, User
from apps.accounts.services.magic_links import (
    InvalidMagicToken,
    consume_whatsapp_login_token,
)
from apps.accounts.services.whatsapp_identity import link_whatsapp_identity_to_user
from apps.wallet.services import grant_free_credits


class PhoneLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, "registration/login.html", {"form": PhoneLoginForm()})

    def post(self, request):
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "dashboard")
            return redirect(next_url)
        return render(request, "registration/login.html", {"form": form})


class PhoneRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, "registration/register.html", {"form": PhoneRegisterForm()})

    def post(self, request):
        form = PhoneRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                phone_number=form.cleaned_data["phone_number"],
                password=form.cleaned_data["password"],
            )
            if form.cleaned_data.get("full_name"):
                user.full_name = form.cleaned_data["full_name"]
                user.save(update_fields=["full_name"])

            Profile.objects.get_or_create(user=user)
            grant_free_credits(user)
            login(request, user)
            return redirect("accounts:onboarding")
        return render(request, "registration/register.html", {"form": form})


class OnboardingView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/onboarding.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.wallet.services import get_balance
        ctx["balance"] = get_balance(self.request.user)
        return ctx

    def post(self, request, *args, **kwargs):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.onboarding_completed = True
        profile.save(update_fields=["onboarding_completed", "updated_at"])
        messages.success(request, "مرحبا بيك! دابا تقدر تبدا تستعمل dwi.ma")
        return redirect("dashboard")


class WhatsAppLoginView(View):
    def get(self, request, token):
        try:
            payload, identity = consume_whatsapp_login_token(token)
        except InvalidMagicToken:
            return HttpResponseBadRequest("Invalid or expired token")

        user = identity.user
        if user is None:
            phone_number = identity.phone_number or f"wa-{identity.wa_id}"
            user = User.objects.create_user(phone_number=phone_number)

        link_whatsapp_identity_to_user(identity, user)
        login(request, user)

        next_url = payload.get("next_url") or "dashboard"
        if next_url == "dashboard":
            return redirect("dashboard")
        return redirect(next_url)

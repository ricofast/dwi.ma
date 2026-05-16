from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.accounts.models import ConsentLog
from apps.accounts.services.consent import log_consent
from apps.payments.models import PaymentTransaction
from apps.payments.services.payments import (
    create_payment_transaction,
    get_active_products,
    start_payment,
)
from apps.wallet.services import get_balance


class ProductsView(LoginRequiredMixin, TemplateView):
    template_name = "payments/products.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["products"] = get_active_products()
        ctx["balance"] = get_balance(self.request.user)
        ctx["active_tab"] = "wallet"
        return ctx


class StartPaymentView(LoginRequiredMixin, TemplateView):
    template_name = "payments/start.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["product_code"] = self.kwargs.get("product_code", "")
        ctx["active_tab"] = "wallet"
        return ctx

    def post(self, request, *args, **kwargs):
        product_code = request.POST.get("product_code", "")
        consent = request.POST.get("consent_accepted") == "true"

        if not consent:
            messages.error(request, "خاصك توافق على شروط الأداء")
            return redirect("payments:products")

        log_consent(
            user=request.user,
            consent_type=ConsentLog.ConsentType.PAYMENT_TERMS,
            accepted=True,
            source="pwa",
            request=request,
            consent_text_snapshot="كنوافق على شروط الأداء واستعمال الكريديات.",
        )

        try:
            tx = create_payment_transaction(request.user, product_code)
            tx = start_payment(tx)
        except (ValueError, Exception) as exc:
            messages.error(request, str(exc))
            return redirect("payments:products")

        if tx.provider_payment_url:
            return redirect(tx.provider_payment_url)

        return redirect("payments:transaction_status", transaction_id=tx.id)


class TransactionStatusView(LoginRequiredMixin, TemplateView):
    template_name = "payments/transaction_status.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["transaction"] = get_object_or_404(
            PaymentTransaction,
            id=self.kwargs["transaction_id"],
            user=self.request.user,
        )
        ctx["active_tab"] = "wallet"
        return ctx


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "payments/success.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tx_id = self.request.GET.get("tx")
        if tx_id:
            ctx["transaction"] = PaymentTransaction.objects.filter(
                id=tx_id, user=self.request.user
            ).first()
        ctx["balance"] = get_balance(self.request.user)
        ctx["active_tab"] = "wallet"
        return ctx


class PaymentFailedView(LoginRequiredMixin, TemplateView):
    template_name = "payments/failed.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tx_id = self.request.GET.get("tx")
        if tx_id:
            ctx["transaction"] = PaymentTransaction.objects.filter(
                id=tx_id, user=self.request.user
            ).first()
        ctx["active_tab"] = "wallet"
        return ctx

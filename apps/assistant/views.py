import hashlib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.conf import settings

from apps.assistant.models import AIJob
from apps.assistant.services.message_generation import generate_message_from_text
from apps.assistant.tasks import explain_text_task
from apps.wallet.services import can_spend, get_balance


class ExplainTextFormView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/explain_text_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_tab"] = "home"
        ctx["balance"] = get_balance(self.request.user)
        return ctx

    def post(self, request, *args, **kwargs):
        text = (request.POST.get("text") or "").strip()
        amount = int(getattr(settings, "CREDITS_COST_TEXT_EXPLANATION", 1))
        if len(text) < 10:
            messages.error(request, "النص خاص يكون فيه على الأقل 10 حروف")
            return self.get(request, *args, **kwargs)
        if not can_spend(request.user, amount):
            messages.error(request, "ماعندكش كريدي كافي")
            return self.get(request, *args, **kwargs)
        job = AIJob.objects.create(
            user=request.user,
            job_type=AIJob.JobType.TEXT_EXPLANATION,
            provider="",
            model="",
            status=AIJob.Status.QUEUED,
            input_hash=hashlib.sha256(text.encode()).hexdigest(),
            input_preview=text[:500],
            prompt_version="",
        )
        explain_text_task.delay(
            str(request.user.id),
            text,
            {"output_language": "darija_arabic", "job_id": str(job.id)},
        )
        return redirect("assistant:text_processing", job_id=job.id)


class TextProcessingView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/text_processing.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["job"] = get_object_or_404(
            AIJob, id=self.kwargs["job_id"], user=self.request.user
        )
        ctx["active_tab"] = "home"
        return ctx


class TextResultView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/text_result.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        job = get_object_or_404(
            AIJob, id=self.kwargs["job_id"], user=self.request.user
        )
        ctx["job"] = job
        ctx["result"] = job.result_json or {}
        ctx["active_tab"] = "home"
        return ctx


class GenerateMessageFormView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/generate_message_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_tab"] = "write"
        ctx["balance"] = get_balance(self.request.user)
        return ctx

    def post(self, request, *args, **kwargs):
        try:
            out = generate_message_from_text(
                request.user,
                request.POST.get("input_text"),
                request.POST.get("target_format"),
                request.POST.get("tone", "polite"),
            )
            return redirect("assistant:message_result", job_id=out["job"].id)
        except Exception as exc:
            messages.error(request, str(exc))
            return self.get(request, *args, **kwargs)


class MessageResultView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/message_result.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        job = get_object_or_404(
            AIJob, id=self.kwargs["job_id"], user=self.request.user
        )
        ctx["job"] = job
        ctx["result"] = job.result_json or {}
        ctx["active_tab"] = "write"
        return ctx

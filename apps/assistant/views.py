import hashlib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.assistant.models import AIJob
from apps.assistant.tasks import explain_text_task
from apps.wallet.services import can_spend


class ExplainTextFormView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/explain_text_form.html"

    def post(self, request, *args, **kwargs):
        text = (request.POST.get("text") or "").strip()
        if len(text) < 10:
            messages.error(request, "النص خاص يكون فيه على الأقل 10 حروف")
            return self.get(request, *args, **kwargs)
        if not can_spend(request.user, 1):
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
        explain_text_task.delay(str(request.user.id), text, {"output_language": "darija_arabic", "job_id": str(job.id)})
        return redirect("assistant:text_processing", job_id=job.id)


class TextProcessingView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/text_processing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = get_object_or_404(AIJob, id=self.kwargs["job_id"], user=self.request.user)
        return context


class TextResultView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/text_result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = get_object_or_404(AIJob, id=self.kwargs["job_id"], user=self.request.user)
        context["job"] = job
        context["result"] = job.result_json or {}
        return context

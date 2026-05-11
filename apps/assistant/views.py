from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.assistant.models import AIJob


class ExplainTextFormView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/explain_text_form.html"


class TextProcessingView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/text_processing.html"


class TextResultView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/text_result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = get_object_or_404(AIJob, id=self.kwargs["job_id"], user=self.request.user)
        context["job"] = job
        context["result"] = job.result_json or {}
        return context

import hashlib
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from apps.assistant.models import AIJob
from apps.assistant.tasks import explain_text_task
from apps.wallet.services import can_spend
from apps.assistant.services.message_generation import generate_message_from_text

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
        job = AIJob.objects.create(user=request.user,job_type=AIJob.JobType.TEXT_EXPLANATION,provider="",model="",status=AIJob.Status.QUEUED,input_hash=hashlib.sha256(text.encode()).hexdigest(),input_preview=text[:500],prompt_version="")
        explain_text_task.delay(str(request.user.id), text, {"output_language": "darija_arabic", "job_id": str(job.id)})
        return redirect("assistant:text_processing", job_id=job.id)

class TextProcessingView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/text_processing.html"
    def get_context_data(self, **kwargs):
        c=super().get_context_data(**kwargs); c["job"]=get_object_or_404(AIJob,id=self.kwargs["job_id"],user=self.request.user); return c

class TextResultView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/text_result.html"
    def get_context_data(self, **kwargs):
        c=super().get_context_data(**kwargs); job=get_object_or_404(AIJob,id=self.kwargs["job_id"],user=self.request.user); c["job"]=job; c["result"]=job.result_json or {}; return c

class GenerateMessageFormView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/generate_message_form.html"
    def post(self, request, *args, **kwargs):
        try:
            out = generate_message_from_text(request.user, request.POST.get("input_text"), request.POST.get("target_format"), request.POST.get("tone", "polite"))
            return redirect("assistant:message_result", job_id=out["job"].id)
        except Exception as exc:
            messages.error(request, str(exc)); return self.get(request,*args,**kwargs)

class MessageResultView(LoginRequiredMixin, TemplateView):
    template_name = "assistant/message_result.html"
    def get_context_data(self, **kwargs):
        c=super().get_context_data(**kwargs); job=get_object_or_404(AIJob,id=self.kwargs["job_id"],user=self.request.user); c["job"]=job; c["result"]=job.result_json or {}; return c

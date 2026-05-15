from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.conf import settings
from apps.accounts.models import ConsentLog
from apps.accounts.services.consent import log_consent
from apps.audio.models import VoiceNote, TranscriptionJob
from apps.audio.services.audio import create_voice_note
from apps.audio.services.transcription import transcribe_voice_note
from apps.wallet.services import get_balance


class AudioUploadView(LoginRequiredMixin, TemplateView):
    template_name = "audio/upload.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["credit"] = int(getattr(settings, "CREDITS_COST_VOICE_MESSAGE", 1))
        ctx["active_tab"] = "home"
        ctx["balance"] = get_balance(self.request.user)
        return ctx

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")
        consent_accepted = request.POST.get("consent_accepted") == "true"

        if not uploaded_file:
            messages.error(request, "خاصك تختار تسجيل صوتي")
            return self.get(request, *args, **kwargs)

        if not consent_accepted:
            messages.error(request, "خاصك توافق على معالجة التسجيل الصوتي باش نكملو")
            return self.get(request, *args, **kwargs)

        log_consent(
            user=request.user,
            consent_type=ConsentLog.ConsentType.AUDIO_PROCESSING,
            accepted=True,
            source="pwa",
            request=request,
            consent_text_snapshot="كنوافق أن dwi.ma يعالج هاد التسجيل الصوتي باش يحولو لنص.",
        )

        try:
            voice_note = create_voice_note(request.user, uploaded_file, source="pwa")
        except ValidationError as exc:
            messages.error(request, "; ".join(exc.messages))
            return self.get(request, *args, **kwargs)

        job = transcribe_voice_note(voice_note.id, user=request.user)
        return redirect("audio:processing", voice_note_id=voice_note.id)


class AudioProcessingView(LoginRequiredMixin, TemplateView):
    template_name = "audio/processing.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        vn = get_object_or_404(
            VoiceNote,
            id=self.kwargs["voice_note_id"],
            user=self.request.user,
        )
        ctx["voice_note"] = vn
        ctx["active_tab"] = "home"
        return ctx


class TranscriptionResultView(LoginRequiredMixin, TemplateView):
    template_name = "audio/transcription_result.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        vn = get_object_or_404(
            VoiceNote,
            id=self.kwargs["voice_note_id"],
            user=self.request.user,
        )
        tj = TranscriptionJob.objects.filter(
            voice_note=vn
        ).order_by("-created_at").first()
        ctx["voice_note"] = vn
        ctx["transcription"] = tj
        ctx["balance"] = get_balance(self.request.user)
        ctx["active_tab"] = "home"
        return ctx

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.accounts.models import ConsentLog
from apps.accounts.services.consent import log_consent
from apps.documents.models import UploadedDocument
from apps.documents.services.extraction import (
    calculate_file_hash,
    extract_text,
    validate_document_file,
)
from apps.wallet.services import get_balance


class UploadPageView(LoginRequiredMixin, TemplateView):
    template_name = "documents/upload.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_tab"] = "documents"
        ctx["balance"] = get_balance(self.request.user)
        return ctx

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")
        consent_accepted = request.POST.get("consent_accepted") == "true"

        if not uploaded_file:
            messages.error(request, "خاصك تختار وثيقة")
            return self.get(request, *args, **kwargs)

        if not consent_accepted:
            messages.error(request, "خاصك توافق على معالجة الوثيقة باش نكملو")
            return self.get(request, *args, **kwargs)

        log_consent(
            user=request.user,
            consent_type=ConsentLog.ConsentType.DOCUMENT_PROCESSING,
            accepted=True,
            source="pwa",
            request=request,
            consent_text_snapshot="كنوافق أن dwi.ma يعالج هاد الوثيقة باش يشرحها ليا. نقدر نمسحها من بعد.",
        )

        try:
            file_type = validate_document_file(uploaded_file)
        except ValidationError as exc:
            messages.error(request, "; ".join(exc.messages))
            return self.get(request, *args, **kwargs)

        document = UploadedDocument.objects.create(
            user=request.user,
            original_filename=uploaded_file.name,
            file=uploaded_file,
            file_type=file_type,
            file_size=uploaded_file.size,
            sha256_hash=calculate_file_hash(uploaded_file),
            source="pwa",
            status=UploadedDocument.Status.UPLOADED,
        )

        messages.success(request, "تم رفع الوثيقة بنجاح")
        return redirect("document:document_detail", document_id=document.id)


class UserDocumentMixin(LoginRequiredMixin):
    def get_document(self):
        return get_object_or_404(
            UploadedDocument,
            id=self.kwargs["document_id"],
            user=self.request.user,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["document"] = self.get_document()
        ctx["active_tab"] = "documents"
        return ctx


class DocumentDetailView(UserDocumentMixin, TemplateView):
    template_name = "documents/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        doc = ctx["document"]
        ctx["balance"] = get_balance(self.request.user)
        ctx["can_extract"] = doc.status == UploadedDocument.Status.UPLOADED
        ctx["can_explain"] = doc.status == UploadedDocument.Status.EXTRACTED
        ctx["has_analysis"] = hasattr(doc, "analysis")
        return ctx


class ExtractionResultView(UserDocumentMixin, TemplateView):
    template_name = "documents/extraction_result.html"

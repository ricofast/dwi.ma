from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import UploadedDocument


class UploadPageView(LoginRequiredMixin, TemplateView):
    template_name = "documents/upload.html"


class UserDocumentMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["document"] = get_object_or_404(UploadedDocument, id=self.kwargs["document_id"], user=self.request.user)
        return context


class DocumentDetailView(UserDocumentMixin, TemplateView):
    template_name = "documents/detail.html"


class ExtractionResultView(UserDocumentMixin, TemplateView):
    template_name = "documents/extraction_result.html"

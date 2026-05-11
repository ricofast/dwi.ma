from django.urls import path

from .views import DocumentDetailView, ExtractionResultView, UploadPageView

app_name = "document"

urlpatterns = [
    path("upload/", UploadPageView.as_view(), name="document_upload"),
    path("<uuid:document_id>/", DocumentDetailView.as_view(), name="document_detail"),
    path("<uuid:document_id>/result/", ExtractionResultView.as_view(), name="document_extraction_result"),
]

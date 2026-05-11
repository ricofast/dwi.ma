from django.urls import path

from .views import document_detail, extraction_result, upload_page

# app_name = "documents"

urlpatterns = [
    path("upload/", upload_page, name="document_upload"),
    path("<uuid:document_id>/", document_detail, name="document_detail"),
    path("<uuid:document_id>/result/", extraction_result, name="document_extraction_result"),
]

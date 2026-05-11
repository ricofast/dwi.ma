from django.urls import path

from apps.assistant.views import ExplainTextFormView, TextProcessingView, TextResultView

app_name = "assistant"

urlpatterns = [
    path("explain-text/", ExplainTextFormView.as_view(), name="explain_text_form"),
    path("text-processing/<uuid:job_id>/", TextProcessingView.as_view(), name="text_processing"),
    path("text-result/<uuid:job_id>/", TextResultView.as_view(), name="text_result"),
]

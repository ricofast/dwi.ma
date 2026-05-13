from django.urls import path
from apps.assistant.views import ExplainTextFormView, TextProcessingView, TextResultView, GenerateMessageFormView, MessageResultView
app_name = "assistant"
urlpatterns = [
    path("explain-text/", ExplainTextFormView.as_view(), name="explain_text_form"),
    path("text-processing/<uuid:job_id>/", TextProcessingView.as_view(), name="text_processing"),
    path("text-result/<uuid:job_id>/", TextResultView.as_view(), name="text_result"),
    path("generate-message/", GenerateMessageFormView.as_view(), name="generate_message_form"),
    path("message-result/<uuid:job_id>/", MessageResultView.as_view(), name="message_result"),
]

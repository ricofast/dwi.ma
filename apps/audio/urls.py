from django.urls import path

from .views import AudioProcessingView, AudioUploadView, TranscriptionResultView

app_name = "audio"

urlpatterns = [
    path("upload/", AudioUploadView.as_view(), name="upload"),
    path("<uuid:voice_note_id>/processing/", AudioProcessingView.as_view(), name="processing"),
    path("<uuid:voice_note_id>/result/", TranscriptionResultView.as_view(), name="transcription_result"),
]

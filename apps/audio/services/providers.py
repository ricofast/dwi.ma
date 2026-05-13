import os
from abc import ABC, abstractmethod
from django.conf import settings
from django.core.exceptions import ValidationError

class BaseTranscriptionProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_file_path_or_file, language_hint=None):
        pass

class MockTranscriptionProvider(BaseTranscriptionProvider):
    def transcribe(self, audio_file_path_or_file, language_hint=None):
        return {"transcript": "بغيت نصيفط رسالة اعتذار مهنية", "language_detected": "darija", "confidence": 0.99, "raw_response_json": {"mock": True}}

class OpenAITranscriptionProvider(BaseTranscriptionProvider):
    def transcribe(self, audio_file_path_or_file, language_hint=None):
        if not getattr(settings, "OPENAI_API_KEY", "") and not os.getenv("OPENAI_API_KEY"):
            raise ValidationError("Transcription provider unavailable")
        raise ValidationError("OpenAI transcription unavailable")

def get_transcription_provider():
    p = getattr(settings, "TRANSCRIPTION_PROVIDER", "mock")
    return OpenAITranscriptionProvider() if p == "openai" else MockTranscriptionProvider()

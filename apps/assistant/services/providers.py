import json
import os
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.assistant.models import PromptTemplate

REQUIRED_KEYS = {"document_type", "short_summary_darija", "important_points_darija", "extracted_entities", "unclear_points_darija", "next_steps_darija", "disclaimer_darija", "full_answer_darija"}


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, model: str) -> str:
        pass


class MockLLMProvider(BaseLLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, model: str) -> str:
        return json.dumps({"document_type": "unknown", "short_summary_darija": "هاد شرح مبسط للوثيقة.", "important_points_darija": ["المحتوى موجود فالوثيقة"], "extracted_entities": {"names": [], "dates": [], "amounts": [], "deadlines": [], "obligations": []}, "unclear_points_darija": [], "next_steps_darija": [], "disclaimer_darija": "", "full_answer_darija": "هاد هو الشرح الكامل بالدارجة."}, ensure_ascii=False)


class OpenAIProvider(BaseLLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, model: str) -> str:
        if not os.getenv("OPENAI_API_KEY"):
            raise ValidationError("AI provider unavailable")
        raise ValidationError("OpenAI provider not implemented yet")


class AnthropicProvider(BaseLLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, model: str) -> str:
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValidationError("AI provider unavailable")
        raise ValidationError("Anthropic provider not implemented yet")


class GeminiProvider(BaseLLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, model: str) -> str:
        if not os.getenv("GEMINI_API_KEY"):
            raise ValidationError("AI provider unavailable")
        raise ValidationError("Gemini provider not implemented yet")


def _get_provider(name: str):
    return {"mock": MockLLMProvider(), "openai": OpenAIProvider(), "anthropic": AnthropicProvider(), "gemini": GeminiProvider()}.get(name, MockLLMProvider())


def generate_document_explanation(document_text, provider=None, model=None):
    tmpl = PromptTemplate.objects.filter(name="document_explanation", active=True).order_by("-updated_at").first()
    if not tmpl:
        raise ValidationError("Prompt template unavailable")
    provider_name = provider or getattr(settings, "DEFAULT_LLM_PROVIDER", "mock")
    model_name = model or getattr(settings, "DEFAULT_LLM_MODEL", "mock-1")
    p = _get_provider(provider_name)
    user_prompt = tmpl.user_prompt_template.replace("{{document_text}}", document_text)
    raw = p.generate(tmpl.system_prompt, user_prompt, model_name)

    def parse_or_none(text):
        try:
            data = json.loads(text)
            if not REQUIRED_KEYS.issubset(set(data.keys())):
                return None
            return data
        except Exception:
            return None

    parsed = parse_or_none(raw)
    if parsed is None:
        repair = p.generate("You repair invalid JSON outputs. Return valid JSON only.", f"Repair JSON: {raw}", model_name)
        parsed = parse_or_none(repair)
        if parsed is None:
            raise ValidationError("Failed to parse AI response")
        raw = repair
    return {"raw_response_text": raw, "parsed_json": parsed, "provider": provider_name, "model": model_name, "prompt_version": tmpl.version}

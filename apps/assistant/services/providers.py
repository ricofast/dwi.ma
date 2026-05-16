import json
import os
from abc import ABC, abstractmethod
from urllib import error as urlerror
from urllib import request as urlrequest

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.assistant.models import PromptTemplate

REQUIRED_KEYS = {"document_type", "short_summary_darija", "important_points_darija", "extracted_entities", "unclear_points_darija", "next_steps_darija", "disclaimer_darija", "full_answer_darija"}


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, user_instruction: str, model: str) -> str:
        pass


class MockLLMProvider(BaseLLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, user_instruction: str, model: str) -> str:
        return json.dumps({"document_type": "unknown", "short_summary_darija": "هاد شرح مبسط للوثيقة.", "important_points_darija": ["المحتوى موجود فالوثيقة"], "extracted_entities": {"names": [], "dates": [], "amounts": [], "deadlines": [], "obligations": []}, "unclear_points_darija": [], "next_steps_darija": [], "disclaimer_darija": "", "full_answer_darija": "هاد هو الشرح الكامل بالدارجة."}, ensure_ascii=False)


class OpenAIProvider(BaseLLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, user_instruction: str, model: str) -> str:
        api_key = os.getenv("DJANGO_OPENAI") or getattr(settings, "OPENAI_API_KEY", "")
        if not api_key:
            raise ValidationError("AI provider unavailable")
        payload = {
            "model": model,
            "input": [
                {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                {"role": "user", "content": [{"type": "input_text", "text": user_prompt}]},
            ],
            "text": {"format": {"type": "text"}},
        }
        req = urlrequest.Request(
            url="https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlrequest.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except (urlerror.URLError, urlerror.HTTPError) as exc:
            raise ValidationError(f"OpenAI request failed: {exc}")
        text = data.get("output_text")
        if text:
            return text
        output = data.get("output", [])
        for item in output:
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    return content["text"]
        raise ValidationError("OpenAI empty response")


class AnthropicProvider(BaseLLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, user_instruction: str, model: str) -> str:
        api_key = os.getenv("DJANGO_ANTHROPICAPI") or getattr(settings, "ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ValidationError("AI provider unavailable")
        payload = {
            "model": model,
            "max_tokens": 2500,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        }
        req = urlrequest.Request(
            url="https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            method="POST",
        )
        try:
            with urlrequest.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except (urlerror.URLError, urlerror.HTTPError) as exc:
            raise ValidationError(f"Anthropic request failed: {exc}")
        for part in data.get("content", []):
            if part.get("type") == "text" and part.get("text"):
                return part["text"]
        raise ValidationError("Anthropic empty response")


class GeminiProvider(BaseLLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, user_instruction: str, model: str) -> str:
        api_key = os.getenv("DJANGO_GEMINIAPI") or getattr(settings, "GEMINI_API_KEY", "")
        if not api_key:
            raise ValidationError("AI provider unavailable")
        # payload = {
        #     "system_instruction": {"parts": [{"text": system_prompt}]},
        #     "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        #     "generationConfig": {"temperature": 0.2},
        # }
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "[CONTEXT / DOCUMENT DATA START]\n"
                                f"{user_prompt}\n"
                                "[CONTEXT / DOCUMENT DATA END]\n\n"
                                "[USER OBJECTIVE / INSTRUCTION]\n"
                                f"{user_instruction}"
                            )
                        }
                    ]
                }
            ],
            "systemInstruction": {
                "parts": [
                    {"text": system_prompt}
                    # Insert your system prompt here
                ]
            },
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2,
                "maxOutputTokens": 2000,
                # Define the exact structural schema directly in the JSON body
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "explanation": {
                            "type": "STRING",
                            "description": "The primary explanation, translated content, or drafted text in simple Moroccan Darija (Arabic script)."
                        },
                        "missing_information": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"},
                            "description": "Missing elements required from the user to complete the task accurately."
                        },
                        "is_unclear": {
                            "type": "BOOLEAN",
                            "description": "Flag true if the user's uploaded document content or message prompt is entirely unintelligible."
                        },
                        "unclear_message": {
                            "type": "STRING",
                            "description": "If is_unclear is True, must contain exactly: 'هاد النقطة ما واضحةش فالمعطيات اللي توصلت بها.'"
                        },
                        "disclaimer": {
                            "type": "STRING",
                            "description": "Mandatory exact warning block for legal or official documents."
                        }
                    },
                    "required": ["explanation", "missing_information", "is_unclear", "unclear_message", "disclaimer"]
                }
            }
        }
        req = urlrequest.Request(
            url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlrequest.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except (urlerror.URLError, urlerror.HTTPError) as exc:
            raise ValidationError(f"Gemini request failed: {exc}")
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                if part.get("text"):
                    return part["text"]
        raise ValidationError("Gemini empty response")


def _get_provider(name: str):
    return {"mock": MockLLMProvider(), "openai": OpenAIProvider(), "anthropic": AnthropicProvider(), "gemini": GeminiProvider()}.get(name, MockLLMProvider())


def generate_document_explanation(document_text, provider=None, model=None):
    tmpl = PromptTemplate.objects.filter(name="document_explanation", active=True).order_by("-updated_at").first()
    if not tmpl:
        raise ValidationError("Prompt template unavailable")
    provider_name = provider or getattr(settings, "DEFAULT_LLM_PROVIDER", "mock")
    model_name = model or getattr(settings, "DEFAULT_LLM_MODEL", "mock-1")
    p = _get_provider(provider_name)
    instructions = ""
    user_prompt = tmpl.user_prompt_template.replace("{{document_text}}", document_text)
    raw = p.generate(tmpl.system_prompt, user_prompt, instructions, model_name)

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

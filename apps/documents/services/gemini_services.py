import os
import json
import base64
import urllib.request as urlrequest
from google import genai
from google.genai import types
from uuid import UUID

from django.conf import settings

from apps.assistant.schemas.prompts import DWI_SYSTEM_PROMPT
from apps.documents.services.schemas import GeminiDwiResponseSchema


llm_provider = getattr(settings, "DEFAULT_LLM_PROVIDER")
llm_model = getattr(settings, "DEFAULT_LLM_MODEL")

class GeminiDwiRestEngine:
    def __init__(self):
        self.api_key = getattr(settings, "GEMINI_API_KEY")
        self.model = llm_model
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def execute_analysis(self, instruction: str, text_context: str = None, file_b64: str = None,
                         mime_type: str = None) -> dict:
        """
        Communicates with Gemini 3.1 Pro using raw HTTP POST via urllib.
        """
        # 1. Structure the initial text instruction part
        prompt_text = f"[USER OBJECTIVE / INSTRUCTION]\n{instruction}\n"

        parts_list = []

        # 2. Strategy Split: Text context vs. Raw Multimodal File Data
        if text_context:
            prompt_text += f"\n[CONTEXT DATA START]\n{text_context}\n[CONTEXT DATA END]"
            parts_list.append({"text": prompt_text})
        elif file_b64 and mime_type:
            prompt_text += "\n[CRITICAL NOTE]: Pre-extraction failed. Analyze this raw file directly to fulfill the user request."
            parts_list.append({"text": prompt_text})
            # Inject the raw binary asset directly into the multi-part tracking array
            parts_list.append({
                "inlineData": {
                    "mimeType": mime_type,
                    "data": file_b64
                }
            })
        else:
            raise ValueError("Invalid payload: Provide either text_context or file execution variants.")

        # 3. Construct standard OpenAPI JSON REST payload mapping to Google specifications
        payload = {
            "contents": [{"parts": parts_list}],
            "systemInstruction": {
                "parts": [{"text": DWI_SYSTEM_PROMPT}]
            },
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2,
                "maxOutputTokens": 3000,
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "explanation": {
                            "type": "STRING",
                            "description": "The primary explanation, translation, or drafted document in simple Moroccan Darija (Arabic script)."
                        },
                        "missing_information": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"},
                            "description": "Missing variables needed from the user to complete the task accurately."
                        },
                        "is_unclear": {
                            "type": "BOOLEAN",
                            "description": "True if the context document or audio is unintelligible or unreadable."
                        },
                        "unclear_message": {
                            "type": "STRING",
                            "description": "Must be exactly 'هاد النقطة ما واضحةش فالمعطيات اللي توصلت بها.' if is_unclear is True."
                        },
                        "disclaimer": {
                            "type": "STRING",
                            "description": "Mandatory disclaimer warning for legal/financial domains."
                        }
                    },
                    "required": ["explanation", "missing_information", "is_unclear", "unclear_message", "disclaimer"]
                }
            }
        }

        # 4. Dispatch transaction over network boundaries
        req = urlrequest.Request(
            url=self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            },
            method="POST"
        )

        try:
            with urlrequest.urlopen(req, timeout=30) as response:
                api_response = json.loads(response.read().decode("utf-8"))
                # Unpack native structural nested layer returns
                raw_text_output = api_response['candidates'][0]['content']['parts'][0]['text']
                return json.loads(raw_text_output)

        except Exception as e:
            # Resilient fallback handler to prevent pipeline lock
            return {
                "explanation": "Smeh lia, waqa3 mouchkil f l-sistim dial l-weta2iq. Chwiya w t3awed.",
                "missing_information": [str(e)],
                "is_unclear": True,
                "unclear_message": "هاد النقطة ما واضحةش فالمعطيات اللي توصلت بها.",
                "disclaimer": ""
            }


def call_gemini_api(document):

    # 1. Extract binary and detect MIME type
    # doc_instance.file is your Django FileField
    file_bytes = document.file.read()
    file_name = document.file.name
    file_type = document.file_type

    if file_type == "pdf":
        mime_type = 'application/pdf'
    elif file_type == "jpeg":
        mime_type = 'image/jpeg'
    elif file_type == "png":
        mime_type = 'image/png'
    else:
        mime_type = 'application/octet-stream'

    file_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
    api_key = os.getenv("DJANGO_GEMINIAPI") or getattr(settings, "GEMINI_API_KEY", "")
    client = genai.Client(api_key=api_key)

    # 2. Request Analysis
    response = client.models.generate_content(
        model=llm_model,
        contents=[
            "Instruction: Explain this document in simple Moroccan Darija.",
            file_part
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GeminiDwiResponseSchema,
            system_instruction=DWI_SYSTEM_PROMPT
        )
    )

    # 3. Return parsed object (GeminiDwiResponseSchema)
    return response.parsed, response

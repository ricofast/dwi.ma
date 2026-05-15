import os
from google import genai
from google.genai import types
from django.conf import settings
from apps.assistant.schemas.schemas import GeminiDwiResponseSchema
from apps.assistant.schemas.prompts import DWI_SYSTEM_PROMPT, build_user_prompt


class GeminiDwiEngine:
    def __init__(self):
        # The new SDK initialization pattern
        api_key = getattr(settings, "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
        self.client = genai.Client(api_key=api_key)

        # Swapping infrastructure over to Gemini 3.1 Pro
        self.model_name = "gemini-3.1-pro"

    def process_payload(self, raw_text: str, instruction: str) -> GeminiDwiResponseSchema:
        """
        Queries Gemini 3.1 Pro using native structural execution tracking.
        """
        user_content = build_user_prompt(extracted_text=raw_text, custom_instruction=instruction)

        # Build execution configuration via the unified genai type definitions
        config = types.GenerateContentConfig(
            system_instruction=DWI_SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=GeminiDwiResponseSchema,
            temperature=0.2,
            max_output_tokens=2000
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_content,
                config=config
            )

            # The SDK handles data extraction under-the-hood.
            # response.parsed is fully loaded as a GeminiDwiResponseSchema instance.
            return response.parsed

        except Exception as e:
            # Safe pipeline isolation recovery matrix
            return GeminiDwiResponseSchema(
                explanation="Smeh lia, waqa3 mouchkil sghir f l-sistim. Chwiya w t3awed t-sift.",
                missing_information=[str(e)],
                is_unclear=True,
                unclear_message="هاد النقطة ما واضحةش فالمعطيات اللي توصلت بها."
            )
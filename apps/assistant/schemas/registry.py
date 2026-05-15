# apps/assistant/schemas/registry.py

from apps.assistant.schemas.document_explanation import DOCUMENT_EXPLANATION_SCHEMA
from apps.assistant.schemas.text_explanation import TEXT_EXPLANATION_SCHEMA
from apps.assistant.schemas.message_generation import MESSAGE_GENERATION_SCHEMA
from apps.assistant.schemas.complaint_generation import COMPLAINT_GENERATION_SCHEMA


SCHEMA_REGISTRY = {
    "document_explanation": DOCUMENT_EXPLANATION_SCHEMA,
    "text_explanation": TEXT_EXPLANATION_SCHEMA,
    "message_generation": MESSAGE_GENERATION_SCHEMA,
    "complaint_generation": COMPLAINT_GENERATION_SCHEMA,
}


def get_output_schema(service_name: str) -> dict:
    try:
        return SCHEMA_REGISTRY[service_name]
    except KeyError as exc:
        raise ValueError(f"Unknown output schema: {service_name}") from exc
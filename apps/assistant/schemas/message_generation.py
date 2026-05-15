# apps/assistant/schemas/message_generation.py

MESSAGE_GENERATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "service",
        "detected_intent_darija",
        "target_format",
        "tone",
        "output_language",
        "missing_information",
        "used_placeholders",
        "suggested_subject",
        "generated_message",
        "short_version",
        "notes_darija",
        "safety_adjustments_darija",
        "confidence_level",
    ],
    "properties": {
        "service": {
            "type": "string",
            "enum": ["message_generation"],
        },
        "detected_intent_darija": {
            "type": "string",
            "description": "Short Darija description of what the user wants to communicate.",
        },
        "target_format": {
            "type": "string",
            "enum": [
                "professional_french_email",
                "professional_arabic_message",
                "polished_darija_whatsapp",
                "short_reply",
                "supplier_message",
                "customer_message",
                "administrative_request",
                "school_message",
                "job_application_message",
            ],
        },
        "tone": {
            "type": "string",
            "enum": [
                "neutral",
                "polite",
                "polite_firm",
                "friendly",
                "formal",
                "urgent_but_respectful",
            ],
        },
        "output_language": {
            "type": "string",
            "enum": [
                "french",
                "arabic",
                "darija",
                "mixed",
            ],
        },
        "missing_information": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Important missing details the user did not provide.",
        },
        "used_placeholders": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Placeholders inserted into the generated message, e.g. [الاسم], [التاريخ].",
        },
        "suggested_subject": {
            "type": "string",
            "description": "Suggested subject line if the output is an email or formal message. Empty string if not applicable.",
        },
        "generated_message": {
            "type": "string",
            "description": "The final ready-to-copy generated message.",
        },
        "short_version": {
            "type": "string",
            "description": "Shorter version of the message, useful for WhatsApp/SMS. Empty string if not needed.",
        },
        "notes_darija": {
            "type": "string",
            "description": "Short Darija note explaining what was done or what the user should verify.",
        },
        "safety_adjustments_darija": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Any softening, safety, or professionalism adjustments made to the user's original wording.",
        },
        "confidence_level": {
            "type": "string",
            "enum": ["high", "medium", "low"],
        },
    },
}
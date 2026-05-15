# apps/assistant/schemas/text_explanation.py

TEXT_EXPLANATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "service",
        "text_type",
        "detected_language",
        "risk_category",
        "short_summary_darija",
        "simple_explanation_darija",
        "important_points_darija",
        "extracted_entities",
        "what_user_should_do_next_darija",
        "unclear_points_darija",
        "disclaimer_darija",
        "confidence_level",
        "confidence_reason_darija",
        "full_answer_darija",
    ],
    "properties": {
        "service": {
            "type": "string",
            "enum": ["text_explanation"],
        },
        "text_type": {
            "type": "string",
            "description": "Type of text, e.g. email, notice, contract excerpt, admin text, message, invoice note, unknown.",
        },
        "detected_language": {
            "type": "string",
            "description": "Detected language of the provided text, e.g. French, Arabic, Darija, mixed, unknown.",
        },
        "risk_category": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "is_high_risk",
                "categories",
                "reason_darija",
            ],
            "properties": {
                "is_high_risk": {
                    "type": "boolean",
                },
                "categories": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "legal",
                            "medical",
                            "financial",
                            "administrative",
                            "banking",
                            "insurance",
                            "tax",
                            "employment",
                            "education",
                            "housing",
                            "telecom",
                            "other",
                        ],
                    },
                },
                "reason_darija": {
                    "type": "string",
                    "description": "Short Darija explanation of why this text is or is not high-risk.",
                },
            },
        },
        "short_summary_darija": {
            "type": "string",
            "description": "Very short summary in Moroccan Darija.",
        },
        "simple_explanation_darija": {
            "type": "string",
            "description": "Simple Moroccan Darija explanation of the provided text.",
        },
        "important_points_darija": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Main points explained in Darija.",
        },
        "extracted_entities": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "people_names",
                "organizations",
                "dates",
                "amounts",
                "deadlines",
                "reference_numbers",
                "obligations",
            ],
            "properties": {
                "people_names": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "organizations": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "dates": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "amounts": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "deadlines": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "reference_numbers": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "obligations": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
        },
        "what_user_should_do_next_darija": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Practical next steps in Darija, only if supported by the text.",
        },
        "unclear_points_darija": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Unclear or missing points. Use the required Darija unclear phrase when appropriate.",
        },
        "disclaimer_darija": {
            "type": "string",
            "description": "Disclaimer in Darija if text is legal, medical, financial, administrative, or otherwise high-risk.",
        },
        "confidence_level": {
            "type": "string",
            "enum": ["high", "medium", "low"],
        },
        "confidence_reason_darija": {
            "type": "string",
            "description": "Why the confidence is high, medium, or low.",
        },
        "full_answer_darija": {
            "type": "string",
            "description": "Complete user-facing answer in simple Moroccan Darija.",
        },
    },
}
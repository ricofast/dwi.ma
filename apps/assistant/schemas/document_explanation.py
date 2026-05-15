# apps/assistant/schemas/document_explanation.py

DOCUMENT_EXPLANATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "service",
        "document_type",
        "detected_language",
        "risk_category",
        "short_summary_darija",
        "important_points_darija",
        "extracted_entities",
        "what_user_should_do_next_darija",
        "unclear_points_darija",
        "questions_to_ask_darija",
        "disclaimer_darija",
        "confidence_level",
        "confidence_reason_darija",
        "full_answer_darija",
    ],
    "properties": {
        "service": {
            "type": "string",
            "enum": ["document_explanation"],
        },
        "document_type": {
            "type": "string",
        },
        "detected_language": {
            "type": "string",
        },
        "risk_category": {
            "type": "object",
            "additionalProperties": False,
            "required": ["is_high_risk", "categories", "reason_darija"],
            "properties": {
                "is_high_risk": {"type": "boolean"},
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
                            "other",
                        ],
                    },
                },
                "reason_darija": {"type": "string"},
            },
        },
        "short_summary_darija": {
            "type": "string",
        },
        "important_points_darija": {
            "type": "array",
            "items": {"type": "string"},
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
                "addresses",
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
                "addresses": {
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
        },
        "unclear_points_darija": {
            "type": "array",
            "items": {"type": "string"},
        },
        "questions_to_ask_darija": {
            "type": "array",
            "items": {"type": "string"},
        },
        "disclaimer_darija": {
            "type": "string",
        },
        "confidence_level": {
            "type": "string",
            "enum": ["high", "medium", "low"],
        },
        "confidence_reason_darija": {
            "type": "string",
        },
        "full_answer_darija": {
            "type": "string",
        },
    },
}
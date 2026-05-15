# apps/assistant/schemas/complaint_generation.py

COMPLAINT_GENERATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "service",
        "complaint_target",
        "detected_problem_darija",
        "desired_outcome",
        "target_format",
        "tone",
        "missing_information",
        "used_placeholders",
        "suggested_subject",
        "generated_complaint",
        "short_whatsapp_version",
        "escalation_version",
        "evidence_to_attach_darija",
        "next_steps_darija",
        "notes_darija",
        "safety_adjustments_darija",
        "confidence_level",
    ],
    "properties": {
        "service": {
            "type": "string",
            "enum": ["complaint_generation"],
        },
        "complaint_target": {
            "type": "string",
            "enum": [
                "telecom",
                "bank",
                "online_store",
                "delivery_company",
                "supplier",
                "landlord",
                "school",
                "administration",
                "employer",
                "insurance",
                "utility_company",
                "other",
            ],
        },
        "detected_problem_darija": {
            "type": "string",
            "description": "Short Darija summary of the user's problem.",
        },
        "desired_outcome": {
            "type": "string",
            "enum": [
                "refund",
                "repair",
                "explanation",
                "cancellation",
                "compensation",
                "apology",
                "correction",
                "follow_up",
                "replacement",
                "service_activation",
                "other",
            ],
        },
        "target_format": {
            "type": "string",
            "enum": [
                "french_email",
                "arabic_formal_message",
                "darija_whatsapp",
                "short_firm_reply",
                "escalation_message",
            ],
        },
        "tone": {
            "type": "string",
            "enum": [
                "polite",
                "polite_firm",
                "urgent_but_respectful",
            ],
        },
        "missing_information": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Important missing details, e.g. order number, date, customer number.",
        },
        "used_placeholders": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Placeholders used in the generated complaint.",
        },
        "suggested_subject": {
            "type": "string",
            "description": "Suggested complaint subject if email/formal format is used.",
        },
        "generated_complaint": {
            "type": "string",
            "description": "The final ready-to-send complaint.",
        },
        "short_whatsapp_version": {
            "type": "string",
            "description": "Short complaint version suitable for WhatsApp.",
        },
        "escalation_version": {
            "type": "string",
            "description": "More formal escalation version. Empty string if not appropriate.",
        },
        "evidence_to_attach_darija": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Documents/screenshots/proofs the user may attach, based only on the user's complaint.",
        },
        "next_steps_darija": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Practical next steps in Darija.",
        },
        "notes_darija": {
            "type": "string",
            "description": "Short note in Darija about missing info, tone, or how to use the complaint.",
        },
        "safety_adjustments_darija": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Any insults, threats, or unsafe language that were softened or removed.",
        },
        "confidence_level": {
            "type": "string",
            "enum": ["high", "medium", "low"],
        },
    },
}
# apps/assistant/services/schema_validation.py

import json
from jsonschema import validate, ValidationError


class SchemaValidationError(Exception):
    pass


def parse_json_response(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise SchemaValidationError("The AI returned invalid JSON.") from exc


def validate_output_schema(data: dict, schema: dict) -> dict:
    try:
        validate(instance=data, schema=schema)
    except ValidationError as exc:
        raise SchemaValidationError(
            f"The AI output does not match the required schema: {exc.message}"
        ) from exc

    return data


def parse_and_validate(raw_text: str, schema: dict) -> dict:
    data = parse_json_response(raw_text)
    return validate_output_schema(data, schema)
JE_SCHEMA = {
    "type": "object",
    "required": ["date", "memo", "lines"],
    "properties": {
        "date": {"type": "string"},
        "memo": {"type": "string"},
        "lines": {
            "type": "array",
            "minItems": 2,
            "items": {
                "type": "object",
                "required": ["account", "debit", "credit"],
                "properties": {
                    "account": {"type": "string"},
                    "debit": {"type": "number", "minimum": 0},
                    "credit": {"type": "number", "minimum": 0},
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}

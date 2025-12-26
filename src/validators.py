from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .schemas import JE_SCHEMA

def validate_schema(payload: dict) -> None:
    try:
        validate(instance=payload, schema=JE_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Model output failed schema validation: {e.message}") from e

def _money(x: float) -> Decimal:
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def validate_balanced(payload: dict) -> None:
    debits = sum(_money(line["debit"]) for line in payload["lines"])
    credits = sum(_money(line["credit"]) for line in payload["lines"])
    if debits != credits:
        raise ValueError(f"Journal entry is not balanced. Debits={debits} Credits={credits}")

def normalize(payload: dict) -> dict:
    for line in payload["lines"]:
        line["account"] = str(line["account"]).strip()
        line["debit"] = float(_money(line["debit"]))
        line["credit"] = float(_money(line["credit"]))
    payload["memo"] = str(payload["memo"]).strip()
    payload["date"] = str(payload["date"]).strip()
    return payload

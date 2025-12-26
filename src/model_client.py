from __future__ import annotations
import json
import os
from typing import Any

class ModelClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()

    def call_model(self, system: str, user: str, json_schema: dict | None = None) -> dict:
        # No key → safe fallback
        if not self.api_key:
            return self._stub_response()

        try:
            from openai import OpenAI
        except Exception:
            return self._stub_response()

        client = OpenAI(api_key=self.api_key)

        if json_schema:
            response_format: dict[str, Any] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "journal_entry",
                    "strict": True,
                    "schema": json_schema,
                },
            }
        else:
            response_format = {"type": "json_object"}

        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format=response_format,
        )

        content = resp.choices[0].message.content or "{}"
        return json.loads(content)

    def _stub_response(self) -> dict:
        # Balanced example JE
        return {
            "date": "2025-12-26",
            "memo": "Office supplies purchase",
            "lines": [
                {"account": "Office Supplies Expense", "debit": 75.00, "credit": 0.00},
                {"account": "Operating Checking", "debit": 0.00, "credit": 75.00},
            ],
        }

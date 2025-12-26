SYSTEM_PROMPT = """You are an expert accountant.
Create a correct journal entry for the described transaction.
Return ONLY valid JSON. No markdown. No commentary."""

USER_TEMPLATE = """
Entity name: {entity_name}

Transaction description:
{description}

Optional evidence (may be empty):
- PDF excerpt (truncated): {pdf_excerpt}
- CSV hints: {csv_hints}
- CSV top descriptions: {csv_top_descriptions}

Rules:
- Output must be balanced (total debits = total credits).
- Use simple, standard accounts unless entity-specific accounts are obvious from the evidence.
- Amounts must be positive numbers; use 0 for the other side.
- If ambiguous, pick the most reasonable treatment and keep it minimal (2-4 lines).

Output JSON schema:
{{
  "date": "YYYY-MM-DD",
  "memo": "short memo",
  "lines": [
    {{ "account": "Account Name", "debit": 0, "credit": 0 }}
  ]
}}
"""

from __future__ import annotations
import csv
import io
from dataclasses import dataclass

@dataclass
class CsvEvidence:
    rows_preview: list[dict]
    top_descriptions: list[dict]
    hints: list[str]

def _norm(s: str) -> str:
    return (s or "").strip()

def parse_bank_csv(file_bytes: bytes, max_rows: int = 300) -> list[dict]:
    """
    Flexible CSV reader:
    - Accepts bytes from Streamlit uploader
    - Uses DictReader so any header format works
    """
    text = file_bytes.decode("utf-8", errors="ignore")
    f = io.StringIO(text)
    reader = csv.DictReader(f)
    rows: list[dict] = []
    for i, row in enumerate(reader):
        if i >= max_rows:
            break
        cleaned = {k: _norm(v) for k, v in (row or {}).items()}
        rows.append(cleaned)
    return rows

def build_csv_evidence(rows: list[dict]) -> CsvEvidence:
    """
    MVP: detect likely description column and surface hints + common merchants.
    """
    if not rows:
        return CsvEvidence(rows_preview=[], top_descriptions=[], hints=[])

    possible_desc_cols = ["description", "memo", "name", "merchant", "payee", "transaction", "details"]
    lower_keys = {k.lower(): k for k in rows[0].keys()}

    desc_col = None
    for c in possible_desc_cols:
        if c in lower_keys:
            desc_col = lower_keys[c]
            break

    descriptions: list[str] = []
    if desc_col:
        for r in rows:
            if r.get(desc_col):
                descriptions.append(r[desc_col].upper())

    counts: dict[str, int] = {}
    for d in descriptions:
        if not d:
            continue
        counts[d] = counts.get(d, 0) + 1

    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:15]
    top_descriptions = [{"description": d[:80], "count": c} for d, c in top]

    joined = "\n".join(descriptions)
    hints: list[str] = []
    for kw, hint in [
        ("SQUARE", "POS/processor likely (Square)"),
        ("STRIPE", "POS/processor likely (Stripe)"),
        ("PAYROLL", "Payroll activity detected"),
        ("GUSTO", "Payroll provider likely (Gusto)"),
        ("ADP", "Payroll provider likely (ADP)"),
        ("LOAN", "Loan-related activity detected"),
        ("INTEREST", "Interest expense likely"),
        ("ATM", "Cash withdrawals likely"),
        ("WIRE", "Wire activity likely"),
        ("ZELLE", "Zelle transfers likely"),
        ("VENMO", "Venmo activity likely"),
        ("PAYPAL", "PayPal activity likely"),
    ]:
        if kw in joined:
            hints.append(hint)

    return CsvEvidence(
        rows_preview=rows[:25],
        top_descriptions=top_descriptions,
        hints=hints,
    )

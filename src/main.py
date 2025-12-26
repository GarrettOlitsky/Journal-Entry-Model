from __future__ import annotations
import argparse

from .prompts import SYSTEM_PROMPT, USER_TEMPLATE
from .model_client import ModelClient
from .schemas import JE_SCHEMA
from .validators import validate_schema, validate_balanced, normalize
from .excel_writer import write_je_xlsx

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a Journal Entry (Excel) from a transaction description.")
    p.add_argument("--entity", required=True, help="Entity name")
    p.add_argument("--desc", required=True, help="Transaction description")
    p.add_argument("--out", default="Journal_Entry.xlsx", help="Output XLSX")
    return p.parse_args()

def run(
    entity_name: str,
    description: str,
    out_path: str,
    pdf_excerpt: str = "",
    csv_hints: list[str] | None = None,
    csv_top_descriptions: list[dict] | None = None,
) -> dict:
    csv_hints = csv_hints or []
    csv_top_descriptions = csv_top_descriptions or []

    user_prompt = USER_TEMPLATE.format(
        entity_name=entity_name,
        description=description,
        pdf_excerpt=pdf_excerpt,
        csv_hints=csv_hints,
        csv_top_descriptions=csv_top_descriptions,
    )

    client = ModelClient()
    payload = client.call_model(SYSTEM_PROMPT, user_prompt, json_schema=JE_SCHEMA)

    validate_schema(payload)
    validate_balanced(payload)
    payload = normalize(payload)

    write_je_xlsx(payload, out_path)
    return payload

def main() -> None:
    args = parse_args()
    run(args.entity, args.desc, args.out)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()

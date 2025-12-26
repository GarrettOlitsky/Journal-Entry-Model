from __future__ import annotations
import pdfplumber

def extract_text_from_pdf(pdf_path: str, max_pages: int = 2) -> str:
    chunks: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:max_pages]:
            txt = page.extract_text() or ""
            if txt.strip():
                chunks.append(txt)
    return "\n\n".join(chunks).strip()

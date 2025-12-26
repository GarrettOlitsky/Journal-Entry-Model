import os
import tempfile
import streamlit as st

from src.main import run
from src.ingest.pdf_extract import extract_text_from_pdf
from src.ingest.csv_bank import parse_bank_csv, build_csv_evidence

st.set_page_config(page_title="Journal Entry Model", layout="centered")
st.title("Journal Entry Model (LLM → Excel)")
st.caption("Describe a transaction or upload a PDF/CSV. Generates a balanced journal entry in Excel.")

entity = st.text_input("Entity name", value="REGAL ALE")

desc = st.text_area(
    "Transaction description (example: 'Paid $620.55 loan payment to Chase; $120.55 interest; remainder principal.')",
    height=120,
)

uploaded_pdf = st.file_uploader("Optional: Upload a PDF (bank/loan statement, invoice)", type=["pdf"])
uploaded_csv = st.file_uploader("Optional: Upload a CSV (bank export)", type=["csv"])

pdf_excerpt = ""
if uploaded_pdf is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.getbuffer())
        tmp_path = tmp.name

    pdf_excerpt = extract_text_from_pdf(tmp_path, max_pages=2)[:4000]
    os.unlink(tmp_path)

    st.subheader("PDF excerpt (truncated)")
    st.text(pdf_excerpt[:1200])

csv_hints = []
csv_top_descriptions = []
if uploaded_csv is not None:
    rows = parse_bank_csv(uploaded_csv.getvalue())
    ev = build_csv_evidence(rows)
    csv_hints = ev.hints
    csv_top_descriptions = ev.top_descriptions

    st.subheader("CSV detected signals (MVP)")
    st.write({"hints": csv_hints, "top_descriptions": csv_top_descriptions})

    st.subheader("CSV preview")
    st.dataframe(ev.rows_preview)

out_name = st.text_input("Output filename", value="Journal_Entry.xlsx")

if st.button("Generate Journal Entry Excel"):
    payload = run(
        entity_name=entity,
        description=desc,
        out_path=out_name,
        pdf_excerpt=pdf_excerpt,
        csv_hints=csv_hints,
        csv_top_descriptions=csv_top_descriptions,
    )

    st.success("Generated balanced journal entry.")
    st.write(payload)

    with open(out_name, "rb") as f:
        st.download_button(
            "Download Excel",
            data=f,
            file_name=out_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

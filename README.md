# Journal Entry Model (LLM → Excel)

Describe a transaction (or upload a PDF/CSV) and generate a **balanced** journal entry as an Excel file.

## Setup

```bash
git clone https://github.com/GarrettOlitsky/journal-entry-model.git
cd journal-entry-model

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Run (Streamlit)
bash
Copy code
streamlit run app.py
Run (CLI)
bash
Copy code
python -m src.main \
  --entity "REGAL ALE" \
  --desc "Paid $620.55 loan payment to Chase; $120.55 interest; remainder principal." \
  --out "Journal_Entry.xlsx"
LLM (optional)
bash
Copy code
export OPENAI_API_KEY="YOUR_KEY"
export OPENAI_MODEL="gpt-4.1-mini"
If no key is set, the app uses a safe stub response.

yaml
Copy code

---

# 4) `src/__init__.py` (KEEP/REPLACE)
```python
# src package
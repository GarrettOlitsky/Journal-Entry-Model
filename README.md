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

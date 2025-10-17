# AI Text Summarizer

A minimal Streamlit app that summarizes pasted text or content fetched from a URL.

## Quickstart

```bash
# 1) Setup
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) Configure
cp .env.example .env  # add your OPENAI_API_KEY

# 3) Run
streamlit run app.py

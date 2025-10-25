AI Text Summarizer

Summarize text, URLs, or PDFs into clear executive summaries using GPT-4o.

Live: <https://ai-text-summariser.streamlit.app/>
Stack: Python • Streamlit • OpenAI • BeautifulSoup • PyPDF

Features

- Paste text or fetch from URL
- Upload PDFs
- Presets (Executive, Bullets, TL;DR)
- Token & cost estimate

Quickstart
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # add OPENAI_API_KEY and OPENAI_MODEL
streamlit run app.py

Roadmap

- Multi-language
- Save history to Notion/SQLite
- Batch summarize multiple URLs/PDFs

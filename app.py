import io
import os
import streamlit as st
from pypdf import PdfReader

from summarizer import summarize, last_usage
from utils import fetch_url_text

st.set_page_config(page_title="AI Text Summarizer", page_icon="📝", layout="centered")

st.title("📝 AI Text Summarizer")
st.caption("Paste text, a URL, or a PDF. Choose style. Get a great summary.")

# keep state for fetched/parsed text
if "url_text" not in st.session_state:
    st.session_state["url_text"] = ""
if "pdf_text" not in st.session_state:
    st.session_state["pdf_text"] = ""
if "result" not in st.session_state:
    st.session_state["result"] = ""

# -------- Tabs (Input Sources) --------
tab_paste, tab_url, tab_pdf, tab_about = st.tabs(["Paste Text", "From URL", "From PDF", "About"])

with tab_paste:
    raw_text = st.text_area("Input text", height=220, placeholder="Paste article, report, email…")

with tab_url:
    url = st.text_input("Article URL")
    if st.button("Fetch", key="fetch_url"):
        fetched = fetch_url_text(url)
        if fetched:
            st.session_state["url_text"] = fetched
            st.success("Fetched content.")
        else:
            st.warning("Couldn’t extract text from that URL.")
    if st.session_state["url_text"]:
        with st.expander("Preview fetched text"):
            st.write(st.session_state["url_text"][:2000] + ("…" if len(st.session_state["url_text"]) > 2000 else ""))

with tab_pdf:
    pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf:
        reader = PdfReader(io.BytesIO(pdf.read()))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        st.session_state["pdf_text"] = text.strip()
        st.success(f"Loaded {len(reader.pages)} page(s).")
    if st.session_state["pdf_text"]:
        with st.expander("Preview extracted text"):
            t = st.session_state["pdf_text"]
            st.write(t[:2000] + ("…" if len(t) > 2000 else ""))

with tab_about:
    st.markdown(
        """
**What it does**  
Summarizes pasted text, URLs, or PDFs using GPT models.

**How to use**
1) Provide input in one of the tabs.  
2) Pick summary options or choose a preset.  
3) Click **Summarize**.

**Note**  
Extraction from some sites/PDFs can be imperfect. Always verify critical facts.
"""
    )

st.divider()

# -------- Presets & Options --------
preset = st.selectbox("Preset", ["Custom", "Executive", "Bullets", "TL;DR"])

# default options (will be overridden by preset)
length = st.selectbox("Target length", ["1 paragraph", "3–5 bullets", "10 bullets", "Executive summary"])
tone = st.selectbox("Tone", ["neutral", "professional", "casual", "technical"])
fmt = st.selectbox("Format", ["paragraphs", "bullets", "bullets + action items"])

if preset == "Executive":
    length, tone, fmt = "Executive summary", "professional", "bullets + action items"
elif preset == "Bullets":
    length, tone, fmt = "10 bullets", "neutral", "bullets"
elif preset == "TL;DR":
    length, tone, fmt = "1 paragraph", "casual", "paragraphs"

source = st.radio("Source", ["Pasted text", "Fetched URL text", "Uploaded PDF text"], horizontal=True)
content = (
    raw_text if source == "Pasted text"
    else st.session_state["url_text"] if source == "Fetched URL text"
    else st.session_state["pdf_text"]
)

# -------- Action --------
col1, col2 = st.columns([1, 3])
with col1:
    run = st.button("Summarize", type="primary")
with col2:
    if content:
        st.caption(f"Input length: ~{len(content.split())} words")

if run:
    if not content or len(content.split()) < 5:
        st.error("Please provide enough content to summarize.")
    else:
        with st.spinner("Summarizing…"):
            result = summarize(content, length, tone, fmt)
        st.session_state["result"] = result
        st.success("Done!")

# -------- Output --------
if st.session_state["result"]:
    st.markdown("### Summary")
    st.write(st.session_state["result"])

    # token usage / cost estimate (very rough; adjust for your model/prices)
    if last_usage:
        pt, ct, tt = last_usage["prompt"], last_usage["completion"], last_usage["total"]
        price_per_1k = {"gpt-4o-mini": 0.150}  # example rate
        est = (tt / 1000.0) * price_per_1k.get(os.getenv("OPENAI_MODEL", "gpt-4o-mini"), 0.150)
        st.caption(f"Tokens — prompt: {pt}, completion: {ct}, total: {tt} • est. cost ~ ${est:.4f}")

    st.download_button("Download .txt", data=st.session_state["result"], file_name="summary.txt")
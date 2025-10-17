import streamlit as st
from summarizer import summarize
from utils import fetch_url_text, clean_text

st.set_page_config(page_title="AI Text Summarizer", page_icon="📝")

st.title("📝 AI Text Summarizer")
st.caption("Paste text or a URL. Choose style. Get a great summary.")

tab1, tab2, tab3 = st.tabs(["Paste Text", "Paste URL", "About"])

with tab1:
    raw_text = st.text_area("Input text", height=240, placeholder="Paste article, report, email…")

with tab2:
    url = st.text_input("Article URL")
    if st.button("Fetch"):
        fetched = fetch_url_text(url)
        if fetched:
            st.session_state["url_text"] = fetched
            st.success("Fetched content.")
        else:
            st.warning("Couldn’t extract text from that URL.")

    url_text = st.session_state.get("url_text", "")

with tab3:
    st.markdown("""
    ### About
    This is a minimal Streamlit app that summarizes pasted text or content fetched from a URL using OpenAI's GPT models.

    ### Instructions
    1. Paste text or a URL in the respective tabs.
    2. Choose summary options (length, tone, format).
    3. Click "Summarize" to generate the summary.

    ### Note
    This app is for demonstration purposes and may not handle all edge cases in text extraction or summarization.
    """)

# Options
st.subheader("Summary options")
length = st.selectbox("Target length", ["1 paragraph","3–5 bullets","10 bullets","Executive summary"])
tone = st.selectbox("Tone", ["neutral","professional","casual","technical"])
fmt = st.selectbox("Format", ["paragraphs","bullets","bullets + action items"])

# Source selector
source = st.radio("Source", ["Pasted text","Fetched URL text"])
content = raw_text if source == "Pasted text" else url_text

if st.button("Summarize", type="primary"):
    if not content or len(content.split()) < 5:
        st.error("Please provide enough content to summarize.")
    else:
        with st.spinner("Summarizing…"):
            result = summarize(content, length, tone, fmt)
        st.success("Done!")
        st.markdown("### Summary")
        st.write(result)
        st.download_button("Download .txt", data=result, file_name="summary.txt")
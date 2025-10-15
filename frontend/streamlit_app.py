import streamlit as st
import requests

API_URL = st.secrets.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="News Article Summarizer", page_icon="📰")

st.title("📰 News Article Summarizer")

mode = st.radio("Choose input method", ["Enter Text", "Provide URL"], horizontal=True)

text_input = ""
url_input = ""

if mode == "Enter Text":
    text_input = st.text_area("Paste the article text", height=250, placeholder="Paste article text here...")
else:
    url_input = st.text_input("Enter article URL", placeholder="https://example.com/news/article")

if st.button("Summarize"):
    payload = {}
    if mode == "Enter Text":
        if not text_input or len(text_input.strip()) == 0:
            st.error("Please provide some text")
        else:
            payload["text"] = text_input
    else:
        if not url_input or len(url_input.strip()) == 0:
            st.error("Please provide a URL")
        else:
            payload["url"] = url_input

    if payload:
        with st.spinner("Summarizing..."):
            try:
                resp = requests.post(f"{API_URL}/summarize/", json=payload, timeout=120)
                if resp.status_code == 200:
                    data = resp.json()
                    st.subheader("Summary")
                    st.write(data.get("summary", ""))
                else:
                    try:
                        detail = resp.json().get("detail")
                    except Exception:
                        detail = resp.text
                    st.error(f"Error {resp.status_code}: {detail}")
            except Exception as exc:
                st.error(f"Request failed: {exc}")

st.caption("Backend: FastAPI | Model: facebook/bart-large-cnn")

# News Article Summarizer

FastAPI backend + Streamlit frontend using Hugging Face `facebook/bart-large-cnn` to summarize news articles from raw text or URL (with `newspaper3k` / BeautifulSoup extraction).

## Features
- Summarize raw text or fetch article by URL
- Input length capped (~4000 chars)
- Short text guard (<100 chars)
- Modular services for extraction and summarization

## Tech Stack
- FastAPI, Uvicorn
- Transformers (BART), PyTorch
- newspaper3k, BeautifulSoup4, lxml
- Streamlit UI


```

## Notes
- First run will download the `facebook/bart-large-cnn` model.
- If `newspaper3k` fails to parse, the app falls back to BeautifulSoup paragraph extraction.

---
Generated via setup assistant.

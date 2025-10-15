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

## Setup
```bash
# 1) Create venv
python -m venv .venv
# Windows PowerShell
. .venv\Scripts\Activate.ps1

# 2) Install deps
pip install -r requirements.txt
```

## Run Backend (FastAPI)
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
# Health check: http://localhost:8000/health
```

## Run Frontend (Streamlit)
```bash
# Optional: configure API URL (defaults to http://localhost:8000)
# In .streamlit/secrets.toml add:
# API_URL = "http://localhost:8000"

streamlit run frontend/streamlit_app.py
```

## API Usage
```bash
curl -X POST http://localhost:8000/summarize/ \
  -H "Content-Type: application/json" \
  -d '{"text": "<your long article text here>"}'
```

```bash
curl -X POST http://localhost:8000/summarize/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/news/article"}'
```

## Notes
- First run will download the `facebook/bart-large-cnn` model.
- If `newspaper3k` fails to parse, the app falls back to BeautifulSoup paragraph extraction.

---
Generated via setup assistant.

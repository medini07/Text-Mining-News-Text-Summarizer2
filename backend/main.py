from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from .services.extract import extract_text_from_url
from .services.summarize import summarize_text


MAX_INPUT_LEN = 4000
MIN_INPUT_LEN = 100


class SummarizeRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[HttpUrl] = None


class SummarizeResponse(BaseModel):
    summary: str


app = FastAPI(title="News Article Summarizer")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/summarize/", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest) -> SummarizeResponse:
    if not req.text and not req.url:
        raise HTTPException(status_code=400, detail="Provide either text or url")

    source_text: Optional[str] = None

    if req.url:
        try:
            source_text = extract_text_from_url(str(req.url))
        except Exception as exc:  # only convert to 400 with message
            raise HTTPException(status_code=400, detail=f"Failed to extract article: {exc}")

    if req.text:
        source_text = req.text if not source_text else source_text

    if not source_text:
        raise HTTPException(status_code=422, detail="No text found to summarize")

    source_text = source_text.strip()

    if len(source_text) < MIN_INPUT_LEN:
        raise HTTPException(status_code=400, detail="Text is too short to summarize (<100 chars)")

    if len(source_text) > MAX_INPUT_LEN:
        source_text = source_text[:MAX_INPUT_LEN]

    try:
        summary = summarize_text(source_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {exc}")

    return SummarizeResponse(summary=summary)

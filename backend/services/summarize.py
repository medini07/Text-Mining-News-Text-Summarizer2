from __future__ import annotations

from typing import List

from transformers import pipeline


_summarizer = None


def _get_pipeline():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            tokenizer="facebook/bart-large-cnn",
            framework="pt",
            device=-1,
        )
    return _summarizer


def summarize_text(text: str) -> str:
    summarizer = _get_pipeline()
    max_len = 180
    min_len = 60

    chunks: List[str] = [text]

    outputs = summarizer(
        chunks,
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
        truncation=True,
    )

    summaries = [o["summary_text"].strip() for o in outputs]
    return "\n\n".join(summaries)

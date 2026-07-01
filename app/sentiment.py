"""Minimal sentiment utility shipped by the agentic DevOps pipeline demo.

`analyze` is a dependency-free heuristic so the unit tests run fully offline in
CI (no secrets, no network). `fetch_remote_sentiment` shows where a real
Microsoft Foundry model call would plug in later; it is intentionally kept out
of the tested path so the pipeline needs no credentials.
"""

from __future__ import annotations

import requests  # runtime dependency, exercised by fetch_remote_sentiment

_POSITIVE = {"good", "great", "love", "excellent", "amazing", "happy", "best", "brilliant", "fantastic"}
_NEGATIVE = {"bad", "terrible", "hate", "awful", "worst", "sad", "poor"}


def analyze(text: str) -> dict:
    """Return a naive sentiment ``label`` and ``score`` for ``text``.

    The score is (positive_words - negative_words) / total_words, so it stays in
    the range [-1, 1]. This is a stand-in for a real model call, kept simple and
    deterministic so it is easy to unit test.
    """
    if not text or not text.strip():
        raise ValueError("text must be a non-empty string")

    words = [w.strip(".,!?;:").lower() for w in text.split()]
    positive = sum(word in _POSITIVE for word in words)
    negative = sum(word in _NEGATIVE for word in words)
    score = (positive - negative) / max(len(words), 1)

    if score > 0:
        label = "positive"
    elif score < 0:
        label = "negative"
    else:
        label = "neutral"

    return {"label": label, "score": round(score, 3)}


def fetch_remote_sentiment(text: str, endpoint: str, api_key: str) -> dict:
    """Call a remote Microsoft Foundry model endpoint (not used in tests).

    This is where the demo would later swap the local heuristic for a real
    Foundry model. Credentials come from the caller (e.g. an environment
    variable wired through ``${{ secrets.* }}``), never hard-coded.
    """
    response = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

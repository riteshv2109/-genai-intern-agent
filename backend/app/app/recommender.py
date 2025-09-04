import json
from backend.app.app.llm import llm_recommend
from backend.app.app.scoring import score_suggestions, flesch_reading_ease
from backend.app.app.analysis import top_ngrams
from backend.app.app.config import settings
from backend.app.app.utils import backoff_retry
from typing import Dict, Any, List

async def recommend_for_draft(draft: str, cursor_before: str, cursor_after: str, user_profile: Dict, history_keywords: List[str]):
    # Call LLM with retries
    async def call_llm():
        return await llm_recommend(cursor_before, cursor_after, draft, user_profile or {})

    resp = await backoff_retry(call_llm, retries=3, base_ms=settings.BACKOFF_BASE_MS)
    # Parse suggestions
    suggestions = []
    try:
        if isinstance(resp.get("content"), str):
            parsed = json.loads(resp.get("content"))
        else:
            parsed = resp.get("content") or {}
        suggestions = parsed.get("suggestions", [])
    except Exception:
        suggestions = []

    # Build freq map from history + draft ngrams
    freq_map = {}
    for kw in history_keywords or []:
        freq_map[kw.lower()] = freq_map.get(kw.lower(), 0) + 2
    for ng in top_ngrams(draft, k=50):
        freq_map[ng.lower()] = freq_map.get(ng.lower(), 0) + 1

    ranked = score_suggestions(draft, suggestions, user_profile or {}, freq_map)

    # Weak sections detection: long sentences with low FRE
    weak = []
    sentences = [s.strip() for s in draft.split('.') if s.strip()]
    idx = 0
    for s in sentences:
        start = draft.find(s, idx)
        end = start + len(s)
        idx = end
        if len(s.split()) > 20 and flesch_reading_ease(s) < 50:
            weak.append({"start": start, "end": end, "reason": "Hard to read (long/complex)"})

    readability = flesch_reading_ease(draft)

    return {
        "suggestions": ranked[:settings.MAX_SUGGESTIONS],
        "readability": readability,
        "weak_sections": weak,
        "token_usage": resp.get("usage", {})
    }

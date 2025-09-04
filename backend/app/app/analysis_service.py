# small service module used by main endpoint for analyze-blogs
import json
from typing import List
from backend.app.app.analysis import sentiment_scores, top_ngrams
from backend.app.app.llm import llm_analyze_topics
from backend.app.app.utils import backoff_retry
from backend.app.app.config import settings

async def analyze_posts(posts: List[str]):
    results = []
    total_usage = {"prompt_tokens":0, "completion_tokens":0, "total_tokens":0}

    for text in posts:
        sent = sentiment_scores(text)

        async def call_llm():
            return await llm_analyze_topics(text)

        llm_resp = await backoff_retry(call_llm, retries=3, base_ms=settings.BACKOFF_BASE_MS)
        try:
            parsed = json.loads(llm_resp.get("content", "{}"))
            topics = parsed.get("topics", [])
            keywords = list(dict.fromkeys(parsed.get("keywords", []) + top_ngrams(text, 15)))
        except Exception:
            topics = top_ngrams(text, 8)
            keywords = top_ngrams(text, 20)

        usage = llm_resp.get("usage", {})
        for k in total_usage.keys():
            total_usage[k] = total_usage.get(k, 0) + usage.get(k, 0)

        results.append({
            "sentiment": sent,
            "topics": topics,
            "initial_keywords": keywords
        })

    return {"results": results, "token_usage": total_usage}

# app/agent.py
import asyncio
import random
import logging
from typing import Dict, List, Any, Callable
from backend.app.app.recommender import recommend_keywords
from backend.app.app.analysis import analyze_blogs
from backend.app.app.scoring import blog_score

logger = logging.getLogger(__name__)

class BlogAgent:
    def __init__(self, history_blogs: List[str]):
        # Learn from past blogs
        self.patterns = analyze_blogs(history_blogs)
        self.max_retries = 3

    async def suggest_in_real_time(
        self,
        draft: str,
        profile: Dict,
        callback: Callable[[Dict[str, Any]], None]
    ):
        """
        Real-time suggestion loop.
        Calls recommend_keywords periodically as user types.
        """
        attempt = 0
        while attempt < self.max_retries:
            try:
            #    to get recommendations
                rec = recommend_keywords(draft, profile, self.patterns)

            # to compute blog score
                score = blog_score(draft, rec.get("keywords", []), profile)

            # Inline suggestion: append keyword in brackets
                inline_suggestions = [
                    f"[{kw}]" for kw in rec.get("keywords", [])
                ]

                response = {
                    "inline_suggestions": inline_suggestions,
                    "weak_sections": rec.get("weak_sections", []),
                    "score": score,
                }

               
                callback(response)
                break

            except Exception as e:
                attempt += 1
                wait_time = 2 ** attempt + random.uniform(0, 1)
                logger.error(f"Agent failed attempt {attempt}: {e}, retrying in {wait_time:.2f}s")
                await asyncio.sleep(wait_time)



async def run_agentic_loop(draft_stream: List[str], profile: Dict, history_blogs: List[str]):
    agent = BlogAgent(history_blogs)

    async def send_to_ui(payload):
        #  for pushing results to UI
        print("Agent Suggestion:", payload)

    for draft in draft_stream:
        await agent.suggest_in_real_time(draft, profile, send_to_ui)
        await asyncio.sleep(1) 

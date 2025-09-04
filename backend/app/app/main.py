# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from typing import List, Dict, Any
from backend.app.app.schemas import BlogAnalysisRequest, KeywordRecommendRequest
from backend.app.app.security import verify_api_key
from backend.app.app.llm import analyze_blog_with_llm, recommend_keywords_with_llm
from backend.app.app.scoring import blog_score


# FastAPI initialization

app = FastAPI(
    title="Agentic Blog Support System",
    description="""
    Backend service providing blog analysis, scoring, and keyword recommendation
    using AI + heuristics. All endpoints are secured via API key or JWT.
    """,
    version="1.0.0"
)

# Endpoints


@app.post("/api/analyze-blogs", summary="Analyze past blog posts")
async def analyze_blogs(
    request: BlogAnalysisRequest,
    api_key: str = Depends(verify_api_key)
) -> List[Dict[str, Any]]:
    """
    Analyze an array of blog posts.
    Returns for each post:
    - sentiment metrics
    - extracted key topics
    - initial keyword suggestions
    - token usage
    """
    results = []
    for blog in request.blogs:
        llm_result = analyze_blog_with_llm(blog)
        results.append({
            "blog": blog,
            "sentiment": llm_result["analysis"].get("sentiment"),
            "topics": llm_result["analysis"].get("topics"),
            "keywords": llm_result["analysis"].get("keywords"),
            "token_usage": llm_result["token_usage"],
        })
    return results


@app.post("/api/recommend-keywords", summary="Get dynamic keyword suggestions")
async def recommend_keywords(
    request: KeywordRecommendRequest,
    api_key: str = Depends(verify_api_key)
) -> Dict[str, Any]:
    """
    Recommend next keywords/phrases during blog writing.
    Input:
      - draft text (partial or full)
      - cursor context (optional)
      - user profile JSON
    Output:
      - ranked keyword suggestions
      - readability + relevance score (0-100)
      - token usage
    """
    
    llm_result = recommend_keywords_with_llm(
        draft_text=request.draft,
        profile=request.profile or {}
    )

    # Compute scoring 
    score = blog_score(
        text=request.draft,
        keywords=[kw["keyword"] for kw in llm_result["recommendations"]],
        profile=request.profile or {}
    )

    # Return response
    return {
        "recommendations": llm_result["recommendations"],
        "score": score,
        "token_usage": llm_result["token_usage"],
    }



# Root endpoint

@app.get("/", summary="Health check")
async def root() -> Dict[str, str]:
    return {"message": "Agentic Blog Support System API is running"}

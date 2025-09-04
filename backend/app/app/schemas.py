from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class BlogAnalysisRequest(BaseModel):
    posts: List[str] = Field(..., description="Array of existing blog texts")

class SentimentMetrics(BaseModel):
    pos: float
    neu: float
    neg: float
    compound: float

class PostAnalysis(BaseModel):
    sentiment: SentimentMetrics
    topics: List[str]
    initial_keywords: List[str]

class AnalyzeBlogsResponse(BaseModel):
    results: List[PostAnalysis]
    token_usage: Dict[str, int] = Field(default_factory=dict)

class UserProfile(BaseModel):
    preferred_topics: List[str] = []
    reading_level: str = Field("general", description="e.g., beginner, general, advanced")
    banned_words: List[str] = []

class CursorContext(BaseModel):
    before: str = ""
    after: str = ""

class KeywordRecommendRequest(BaseModel):
    draft_text: str
    cursor: Optional[CursorContext] = None
    user_profile: Optional[UserProfile] = None

class Suggestion(BaseModel):
    phrase: str
    reason: str
    relevance_score: float

class WeakSection(BaseModel):
    start: int
    end: int
    reason: str

class RecommendKeywordsResponse(BaseModel):
    suggestions: List[Dict]  # list of Suggestion-like dicts with extra scores
    readability: float
    overall_score: float
    weak_sections: List[WeakSection] = []
    token_usage: Dict[str, int] = Field(default_factory=dict)

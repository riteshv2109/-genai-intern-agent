import pytest
from backend.app.app.scoring import calculate_score


def test_calculate_score_basic():
    draft = "AI helps automate workflows and improve productivity."
    user_profile = {"topics": ["AI", "automation"], "reading_level": "medium"}
    keywords = ["AI", "productivity"]

    score = calculate_score(draft, keywords, user_profile)
    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_score_with_empty_input():
    draft = ""
    user_profile = {"topics": [], "reading_level": "medium"}
    keywords = []

    score = calculate_score(draft, keywords, user_profile)
    assert isinstance(score, int)
    assert score == 0

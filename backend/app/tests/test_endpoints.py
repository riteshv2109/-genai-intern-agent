import pytest
from fastapi.testclient import TestClient
from backend.app.app.main import app

client = TestClient(app)

API_KEY = "test_api_key" 

def test_analyze_blogs():
    response = client.post(
        "/api/analyze-blogs",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "blogs": [
                "AI is transforming how we write blogs.",
                "FastAPI makes backend APIs fast and easy."
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2
    assert "keywords" in data["results"][0]


def test_recommend_keywords():
    response = client.post(
        "/api/recommend-keywords",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "draft": "This blog post is about AI",
            "cursor_context": "AI",
            "user_profile": {"topics": ["AI", "writing"], "reading_level": "medium"}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)
    assert "score" in data
    assert isinstance(data["score"], int)

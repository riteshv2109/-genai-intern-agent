from openai import OpenAI
from typing import Dict, Any
from backend.app.app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_blog_with_llm(blog_text: str) -> Dict[str, Any]:
    """
    Use GPT-4o-mini to analyze a blog post.
    Returns sentiment, key topics, and token usage.
    """
    prompt = f"""
    Analyze the following blog post:
    - Extract 3 key topics
    - Provide sentiment (positive, neutral, negative)
    - Suggest 5 relevant keywords

    Blog Post:
    {blog_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    result_text = response.choices[0].message.content
    usage = response.usage  # contains prompt_tokens, completion_tokens, total_tokens

    return {
        "analysis": result_text,
        "token_usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        },
    }


def recommend_keywords_with_llm(draft_text: str, profile: Dict) -> Dict[str, Any]:
    """
    Suggest next keywords and readability score using GPT.
    """
    prompt = f"""
    The user is writing a blog. Given the draft below, suggest:
    - 5 next keywords or phrases that improve flow
    - Short note on weak areas
    - Readability score (1-10)

    Draft:
    {draft_text}

    User Profile: {profile}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    result_text = response.choices[0].message.content
    usage = response.usage

    return {
        "recommendations": result_text,
        "token_usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        },
    }

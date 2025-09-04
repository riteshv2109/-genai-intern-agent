import re
import math
from collections import Counter
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def flesch_kincaid_grade(text: str) -> float:
    """Compute Flesch-Kincaid Grade Level for readability."""
    sentences = re.split(r'[.!?]', text)
    words = re.findall(r'\w+', text)
    syllables = sum(count_syllables(word) for word in words)
    num_sentences = max(len([s for s in sentences if s.strip()]), 1)
    num_words = max(len(words), 1)

    return 0.39 * (num_words / num_sentences) + 11.8 * (syllables / num_words) - 15.59


def count_syllables(word: str) -> int:
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                count += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False
    return max(count, 1)


def keyword_relevance(text: str, suggested_keywords: List[str]) -> float:
    """Score based on keyword frequency + semantic similarity."""
    if not suggested_keywords:
        return 0.0

    # Frequency-based relevance
    word_counts = Counter(re.findall(r'\w+', text.lower()))
    freq_score = sum(word_counts[k.lower()] for k in suggested_keywords)
    freq_score = min(freq_score / (len(text.split()) + 1), 1.0)  # normalize 0–1

    # Semantic similarity with TF-IDF
    documents = [text] + suggested_keywords
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    cosine_vals = cosine_similarity([vectors[0]], vectors[1:])[0]
    semantic_score = float(sum(cosine_vals) / len(cosine_vals))

    return (freq_score * 0.5 + semantic_score * 0.5) * 100  # scaled 0–100


def user_profile_adjustment(score: float, text: str, profile: Dict) -> float:
    """Adjust score based on user profile (preferred topics, reading level)."""
    if not profile:
        return score

    preferred_topics = profile.get("preferred_topics", [])
    target_level = profile.get("reading_level", None)

    # Boost if text matches preferred topics
    if preferred_topics:
        topic_hits = sum(1 for t in preferred_topics if t.lower() in text.lower())
        score += min(topic_hits * 5, 15)  # up to +15 points

    # Adjust if readability too high/low
    if target_level:
        grade = flesch_kincaid_grade(text)
        if grade > target_level + 3:  # too hard
            score -= 10
        elif grade < target_level - 3:  # too simple
            score -= 5

    return max(0, min(score, 100))  # clamp 0–100


def blog_score(text: str, keywords: List[str], profile: Dict) -> Dict:
    """Return final blog score with breakdown."""
    readability = flesch_kincaid_grade(text)
    keyword_score = keyword_relevance(text, keywords)
    base_score = (keyword_score * 0.6) + (max(0, 100 - readability * 10) * 0.4)
    final_score = user_profile_adjustment(base_score, text, profile)

    return {
        "final_score": round(final_score, 2),
        "keyword_score": round(keyword_score, 2),
        "readability_grade": round(readability, 2),
        "adjusted_for_profile": profile is not None,
    }

import re
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

_STOP = set("""
a an the and or to for of in on with without as is are was were be been being this that it by from at into if then than so such also we you they our your their not no yes very more most much many few several over under between about across after before during within without through up down out off near far any each other own same can will just don't isn't etc
""".split())

_word_re = re.compile(r"[A-Za-z][A-Za-z\-']+")

def top_ngrams(text: str, k: int = 20):
    words = [w.lower() for w in _word_re.findall(text)]
    words = [w for w in words if w not in _STOP and len(w) > 2]
    if not words:
        return []
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    counts = Counter(words + bigrams)
    return [w for w,_ in counts.most_common(k)]

def sentiment_scores(text: str):
    s = sia.polarity_scores(text)
    return {"pos": s["pos"], "neu": s["neu"], "neg": s["neg"], "compound": s["compound"]}

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed_texts(texts: List[str]):
    """
    Returns a numpy array of shape (len(texts), dim)
    Normalized embeddings for cosine similarity use.
    """
    model = get_model()
    emb = model.encode(texts, normalize_embeddings=True)
    return np.array(emb)

def cosine_sim(a: np.ndarray, b: np.ndarray):
    """
    Compute cosine similarity matrix between a (n,d) and b (m,d) returning (n,m)
    """
    return np.matmul(a, b.T)

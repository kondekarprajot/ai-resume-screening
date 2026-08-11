from __future__ import annotations

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity_scores(resume_vectors: np.ndarray, jd_vector: np.ndarray) -> list[float]:
    """Compute cosine similarity between each resume and the job description."""
    scores = cosine_similarity(resume_vectors, jd_vector.reshape(1, -1)).ravel()
    return [float(score) for score in scores]


def to_match_percentage(score: float) -> float:
    """Convert cosine similarity to a readable percentage."""
    bounded = max(0.0, min(1.0, score))
    return round(bounded * 100, 2)

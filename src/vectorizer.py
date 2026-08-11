from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np


VectorizerMode = Literal["tfidf", "sentence-transformer"]


@dataclass
class TextVectorizer:
    """Create numeric representations for resumes and job descriptions."""

    mode: VectorizerMode = "tfidf"
    model_name: str = "all-MiniLM-L6-v2"

    def vectorize(self, documents: list[str]) -> np.ndarray:
        if self.mode == "sentence-transformer":
            return self._sentence_transformer_embeddings(documents)
        return self._tfidf_embeddings(documents)

    def _tfidf_embeddings(self, documents: list[str]) -> np.ndarray:
        from sklearn.feature_extraction.text import TfidfVectorizer

        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        return vectorizer.fit_transform(documents).toarray()

    def _sentence_transformer_embeddings(self, documents: list[str]) -> np.ndarray:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "sentence-transformers is required for advanced embedding mode."
            ) from exc

        model = SentenceTransformer(self.model_name)
        return np.asarray(model.encode(documents, normalize_embeddings=True))

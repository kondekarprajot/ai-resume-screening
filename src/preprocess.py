from __future__ import annotations

import re


_DEFAULT_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
}

_SKILL_NORMALIZATION = {
    "js": "javascript",
    "nodejs": "node.js",
    "node js": "node.js",
    "py": "python",
    "postgres": "postgresql",
    "postgres sql": "postgresql",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
}


def preprocess_text(text: str, remove_stop_words: bool = True) -> str:
    """Clean resume or job description text for matching."""
    normalized = normalize_skills(text.lower())
    normalized = re.sub(r"[^a-z0-9+#.\s-]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    tokens = normalized.split()
    if remove_stop_words:
        tokens = [token for token in tokens if token not in _DEFAULT_STOP_WORDS]

    return " ".join(_simple_lemma(token) for token in tokens)


def normalize_skills(text: str) -> str:
    """Normalize common skill aliases before vectorization."""
    normalized = text
    for source, target in _SKILL_NORMALIZATION.items():
        normalized = re.sub(rf"\b{re.escape(source)}\b", target, normalized)
    return normalized


def _simple_lemma(token: str) -> str:
    """Small dependency-free lemmatization fallback."""
    if len(token) > 4 and token.endswith("ies"):
        return f"{token[:-3]}y"
    if len(token) > 5 and token.endswith("ing"):
        return token[:-3]
    if len(token) > 4 and token.endswith("ed"):
        return token[:-2]
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token

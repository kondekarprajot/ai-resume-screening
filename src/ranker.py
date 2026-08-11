from __future__ import annotations

from dataclasses import dataclass

from src.matcher import to_match_percentage


@dataclass
class ResumeResult:
    file_name: str
    score: float
    match_percentage: float
    matched_skills: list[str]
    missing_skills: list[str]
    status: str


def rank_resumes(
    file_names: list[str],
    scores: list[float],
    matched_skills: list[set[str]],
    missing_skills: list[set[str]],
    threshold: float = 60.0,
) -> list[ResumeResult]:
    """Rank resumes by score and add user-facing screening fields."""
    results = []
    for file_name, score, matched, missing in zip(
        file_names, scores, matched_skills, missing_skills
    ):
        percentage = to_match_percentage(score)
        results.append(
            ResumeResult(
                file_name=file_name,
                score=score,
                match_percentage=percentage,
                matched_skills=sorted(matched),
                missing_skills=sorted(missing),
                status="Shortlist" if percentage >= threshold else "Review",
            )
        )

    return sorted(results, key=lambda result: result.score, reverse=True)

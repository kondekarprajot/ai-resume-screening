from __future__ import annotations

import re


DEFAULT_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "excel",
    "power bi",
    "tableau",
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "data analysis",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "keras",
    "flask",
    "django",
    "streamlit",
    "fastapi",
    "html",
    "css",
    "react",
    "node.js",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "git",
    "linux",
    "api",
    "rest",
    "bert",
    "transformers",
}


def extract_skills(text: str, skills: set[str] | None = None) -> set[str]:
    """Extract known skills from text with phrase-aware matching."""
    skill_set = skills or DEFAULT_SKILLS
    lowered = text.lower()
    found = set()

    for skill in skill_set:
        pattern = rf"(?<![a-z0-9+#.]){re.escape(skill.lower())}(?![a-z0-9+#.])"
        if re.search(pattern, lowered):
            found.add(skill)

    return found


def compare_skills(resume_text: str, job_description: str) -> tuple[set[str], set[str]]:
    """Return matched and missing skills for a resume against a job description."""
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    return matched, missing

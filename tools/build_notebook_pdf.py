from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "AI_Resume_Screening_Jupyter_Notebook.ipynb"
PDF_PATH = ROOT / "AI_Resume_Screening_Jupyter_Notebook_Code.pdf"


NOTEBOOK_CELLS = [
    (
        "markdown",
        "# AI-Based Resume Screening System\n\n"
        "This notebook demonstrates the complete workflow used in the AI-Based Resume Screening System project. "
        "It imports the project modules, preprocesses resume and job description text, generates TF-IDF features, "
        "computes similarity scores, extracts skills, ranks candidates, and displays the result table.",
    ),
    (
        "markdown",
        "## 1. Import Required Libraries",
    ),
    (
        "code",
        """
        from pathlib import Path

        import pandas as pd

        from src.parser import extract_text
        from src.preprocess import preprocess_text
        from src.vectorizer import TextVectorizer
        from src.matcher import compute_similarity_scores
        from src.skill_extractor import compare_skills
        from src.ranker import rank_resumes
        """,
    ),
    (
        "markdown",
        "## 2. Define Job Description\n\n"
        "You can replace this sample job description with any role description.",
    ),
    (
        "code",
        """
        job_description = \"\"\"
        We are looking for a Python developer with SQL, machine learning,
        data analysis, NLP, and Streamlit experience. The candidate should
        understand model development, dashboards, and Git.
        \"\"\"

        print(job_description)
        """,
    ),
    (
        "markdown",
        "## 3. Load Resume Files\n\n"
        "Place resumes inside `data/resumes/`. Supported formats are PDF, DOC, DOCX, and TXT.",
    ),
    (
        "code",
        """
        resume_folder = Path(\"data/resumes\")
        resume_paths = [
            path for path in resume_folder.glob(\"*\")
            if path.is_file() and path.suffix.lower() in {\".pdf\", \".doc\", \".docx\", \".txt\"}
        ]

        resume_paths
        """,
    ),
    (
        "markdown",
        "## 4. Extract Text from Resumes",
    ),
    (
        "code",
        """
        file_names = []
        resume_texts = []

        for path in resume_paths:
            text = extract_text(path)
            file_names.append(path.name)
            resume_texts.append(text)

        print(f\"Loaded {len(resume_texts)} resume(s)\")
        """,
    ),
    (
        "markdown",
        "## 5. Demo Data if No Resume Files Are Available\n\n"
        "This cell allows the notebook to run even before real resumes are added.",
    ),
    (
        "code",
        """
        if not resume_texts:
            file_names = [\"candidate_python.txt\", \"candidate_design.txt\"]
            resume_texts = [
                \"Python developer with SQL, machine learning, pandas, NLP, Streamlit, and Git experience.\",
                \"Graphic designer with branding, illustration, Photoshop, and portfolio presentation experience.\",
            ]

        file_names
        """,
    ),
    (
        "markdown",
        "## 6. Preprocess Resume and Job Description Text",
    ),
    (
        "code",
        """
        processed_resumes = [preprocess_text(text) for text in resume_texts]
        processed_jd = preprocess_text(job_description)

        processed_resumes[:2], processed_jd
        """,
    ),
    (
        "markdown",
        "## 7. Generate TF-IDF Features",
    ),
    (
        "code",
        """
        vectorizer = TextVectorizer(mode=\"tfidf\")
        vectors = vectorizer.vectorize(processed_resumes + [processed_jd])

        resume_vectors = vectors[:-1]
        jd_vector = vectors[-1]

        vectors.shape
        """,
    ),
    (
        "markdown",
        "## 8. Compute Similarity Scores",
    ),
    (
        "code",
        """
        scores = compute_similarity_scores(resume_vectors, jd_vector)
        scores
        """,
    ),
    (
        "markdown",
        "## 9. Extract Matched and Missing Skills",
    ),
    (
        "code",
        """
        matched_skills = []
        missing_skills = []

        for resume_text in resume_texts:
            matched, missing = compare_skills(resume_text, job_description)
            matched_skills.append(matched)
            missing_skills.append(missing)

        list(zip(file_names, matched_skills, missing_skills))
        """,
    ),
    (
        "markdown",
        "## 10. Rank Resumes",
    ),
    (
        "code",
        """
        results = rank_resumes(
            file_names=file_names,
            scores=scores,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            threshold=60,
        )

        results
        """,
    ),
    (
        "markdown",
        "## 11. Display Final Ranked Table",
    ),
    (
        "code",
        """
        ranked_df = pd.DataFrame([
            {
                \"Rank\": index,
                \"Candidate\": result.file_name,
                \"Match Score\": f\"{result.match_percentage}%\",
                \"Status\": result.status,
                \"Extracted Skills\": \", \".join(result.matched_skills) or \"-\",
                \"Missing Skills\": \", \".join(result.missing_skills) or \"-\",
            }
            for index, result in enumerate(results, start=1)
        ])

        ranked_df
        """,
    ),
    (
        "markdown",
        "## 12. Optional Sentence Transformer Model\n\n"
        "Install `requirements-advanced.txt` before running this cell. It gives better semantic matching but may need model download access.",
    ),
    (
        "code",
        """
        # Optional advanced mode:
        # vectorizer = TextVectorizer(
        #     mode=\"sentence-transformer\",
        #     model_name=\"all-MiniLM-L6-v2\",
        # )
        # vectors = vectorizer.vectorize(processed_resumes + [processed_jd])
        # scores = compute_similarity_scores(vectors[:-1], vectors[-1])
        """,
    ),
    (
        "markdown",
        "## 13. Run the Streamlit App\n\n"
        "Run this command in the VS Code terminal to open the web interface.",
    ),
    (
        "code",
        """
        # streamlit run app.py
        """,
    ),
]


def clean_code(source: str) -> str:
    return dedent(source).strip()


def write_notebook() -> None:
    cells = []
    for cell_type, source in NOTEBOOK_CELLS:
        if cell_type == "markdown":
            cells.append(
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": source.splitlines(keepends=True),
                }
            )
        else:
            code = clean_code(source)
            cells.append(
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": code.splitlines(keepends=True),
                }
            )

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.x",
                "mimetype": "text/x-python",
                "codemirror_mode": {"name": "ipython", "version": 3},
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "file_extension": ".py",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=2), encoding="utf-8")


def styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=27,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=18,
        )
    )
    base.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#1F2937"),
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    base.add(
        ParagraphStyle(
            name="NotebookText",
            parent=base["BodyText"],
            fontSize=9.5,
            leading=13,
            spaceAfter=7,
        )
    )
    base.add(
        ParagraphStyle(
            name="Footer",
            parent=base["BodyText"],
            fontSize=8,
            textColor=colors.HexColor("#64748B"),
        )
    )
    return base


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(inch * 0.65, 0.45 * inch, "Jupyter Notebook Code - AI Resume Screening")
    canvas.drawRightString(A4[0] - inch * 0.65, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def markdown_to_paragraphs(text: str, style_map) -> list:
    flowables = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith("# "):
            flowables.append(Paragraph(block[2:], style_map["ReportTitle"]))
        elif block.startswith("## "):
            flowables.append(Paragraph(block[3:], style_map["SectionTitle"]))
        else:
            flowables.append(Paragraph(block.replace("`", ""), style_map["NotebookText"]))
    return flowables


def write_pdf() -> None:
    style_map = styles()
    story = []

    story.append(Spacer(1, 0.25 * inch))
    for cell_type, source in NOTEBOOK_CELLS:
        if cell_type == "markdown":
            story.extend(markdown_to_paragraphs(source, style_map))
        else:
            story.append(
                Preformatted(
                    clean_code(source),
                    ParagraphStyle(
                        name="CodeBlock",
                        fontName="Courier",
                        fontSize=7.2,
                        leading=9.1,
                        backColor=colors.HexColor("#F8FAFC"),
                        borderColor=colors.HexColor("#CBD5E1"),
                        borderWidth=0.5,
                        borderPadding=6,
                        leftIndent=3,
                        rightIndent=3,
                        spaceBefore=3,
                        spaceAfter=8,
                    ),
                    maxLineLength=88,
                )
            )

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.7 * inch,
        title="AI Resume Screening Jupyter Notebook Code",
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    write_notebook()
    write_pdf()
    print(NOTEBOOK_PATH)
    print(PDF_PATH)

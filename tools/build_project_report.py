from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "AI_Based_Resume_Screening_System_Report.pdf"


class ArchitectureFlow(Flowable):
    """Simple vertical architecture flow diagram."""

    def __init__(self) -> None:
        super().__init__()
        self.width = 430
        self.height = 420
        self.steps = [
            "Resume Upload",
            "Job Description Input",
            "Resume Parsing",
            "Text Preprocessing",
            "Feature Engineering / Embeddings",
            "Similarity Computation",
            "Ranking Engine",
            "Results Visualization",
            "Optional LLM Explanation",
        ]

    def draw(self) -> None:
        box_width = 300
        box_height = 28
        x = (self.width - box_width) / 2
        y = self.height - box_height

        self.canv.setFont("Helvetica-Bold", 9)
        for index, step in enumerate(self.steps):
            self.canv.setFillColor(colors.HexColor("#EDF4FF"))
            self.canv.setStrokeColor(colors.HexColor("#2F5597"))
            self.canv.roundRect(x, y, box_width, box_height, 6, stroke=1, fill=1)
            self.canv.setFillColor(colors.HexColor("#1F2937"))
            self.canv.drawCentredString(self.width / 2, y + 9, f"{index + 1}. {step}")

            if index < len(self.steps) - 1:
                arrow_x = self.width / 2
                self.canv.setStrokeColor(colors.HexColor("#64748B"))
                self.canv.line(arrow_x, y - 4, arrow_x, y - 24)
                self.canv.line(arrow_x, y - 24, arrow_x - 4, y - 18)
                self.canv.line(arrow_x, y - 24, arrow_x + 4, y - 18)
            y -= 44


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=24,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["Normal"],
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#1F2937"),
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyJustified",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["BodyText"],
            fontSize=9,
            leading=12,
            spaceAfter=4,
        )
    )
    return styles


def para(text: str, styles, style: str = "BodyJustified") -> Paragraph:
    return Paragraph(text, styles[style])


def bullet_items(items: list[str], styles) -> list[Paragraph]:
    return [Paragraph(f"- {item}", styles["Small"]) for item in items]


def table(data: list[list[str]], widths: list[float] | None = None) -> Table:
    header_style = ParagraphStyle(
        "TableHeader",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )
    cell_style = ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.black,
    )
    wrapped_data = [
        [
            Paragraph(str(cell), header_style if row_index == 0 else cell_style)
            for cell in row
        ]
        for row_index, row in enumerate(data)
    ]

    result = Table(wrapped_data, colWidths=widths, hAlign="LEFT")
    result.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return result


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(inch * 0.7, 0.45 * inch, "AI-Based Resume Screening System")
    canvas.drawRightString(A4[0] - inch * 0.7, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_report() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    story = []

    story.append(Spacer(1, 1.1 * inch))
    story.append(para("AI-Based Resume Screening System", styles, "ReportTitle"))
    story.append(
        para(
            "Project Report on an NLP and Machine Learning based candidate ranking system",
            styles,
            "Subtitle",
        )
    )
    story.append(Spacer(1, 0.4 * inch))
    story.append(
        table(
            [
                ["Project Type", "Artificial Intelligence / Machine Learning"],
                ["Frontend", "Streamlit"],
                ["Core Language", "Python"],
                ["Main Objective", "Rank resumes according to job description relevance"],
            ],
            [1.6 * inch, 4.4 * inch],
        )
    )
    story.append(PageBreak())

    story.append(para("Abstract", styles, "Section"))
    story.append(
        para(
            "The AI-Based Resume Screening System is an intelligent application that automates the initial stage of recruitment by analyzing resumes and matching them against a job description. The system uses Natural Language Processing to parse and preprocess resume content, Machine Learning techniques to represent text numerically, and cosine similarity to calculate how closely each resume matches the job requirements. The final output is a ranked list of candidates with match percentage, extracted skills, missing skills, and shortlist status.",
            styles,
        )
    )

    story.append(para("Introduction", styles, "Section"))
    story.append(
        para(
            "Manual resume screening is time-consuming and can become inconsistent when recruiters evaluate a large number of applications. This project reduces manual effort by providing a structured and repeatable screening workflow. The application supports multiple resume uploads, accepts a job description, analyzes candidate profiles, and presents ranked results through a web interface.",
            styles,
        )
    )

    story.append(para("Objectives", styles, "Section"))
    story.extend(
        bullet_items(
            [
                "Parse resumes from PDF, DOC, DOCX, and TXT formats.",
                "Preprocess resume and job description text for better matching.",
                "Extract relevant technical skills from resumes.",
                "Generate text vectors or semantic embeddings.",
                "Calculate similarity between resumes and job descriptions.",
                "Rank candidates according to match score.",
                "Display results using a user-friendly Streamlit interface.",
            ],
            styles,
        )
    )

    story.append(para("System Architecture", styles, "Section"))
    story.append(ArchitectureFlow())
    story.append(PageBreak())

    story.append(para("Component-Level Architecture", styles, "Section"))
    story.append(
        table(
            [
                ["Component", "Description"],
                ["Input Layer", "Accepts multiple resume files and a job description text input."],
                ["Document Parsing Layer", "Extracts plain text from PDF, DOCX, DOC, and TXT files."],
                ["NLP Preprocessing Layer", "Cleans text using lowercasing, special character removal, stop word removal, lemmatization fallback, and skill normalization."],
                ["Feature Representation Layer", "Creates TF-IDF vectors or Sentence Transformer embeddings."],
                ["Similarity Computation", "Uses cosine similarity to compare each resume with the job description."],
                ["Ranking Engine", "Sorts resumes by score and applies a shortlist threshold."],
                ["Output Layer", "Displays rank, match percentage, matched skills, missing skills, and candidate status."],
            ],
            [1.8 * inch, 4.5 * inch],
        )
    )

    story.append(para("Technology Stack", styles, "Section"))
    story.append(
        table(
            [
                ["Layer", "Technology Used"],
                ["Programming Language", "Python"],
                ["Frontend", "Streamlit"],
                ["Data Handling", "Pandas, NumPy"],
                ["Machine Learning", "scikit-learn"],
                ["Text Matching", "TF-IDF, cosine similarity, Sentence Transformers"],
                ["Document Parsing", "pdfplumber, PyMuPDF, python-docx, Apache Tika"],
                ["Optional Explainability", "SHAP, LIME, LLM-generated explanations"],
            ],
            [1.9 * inch, 4.4 * inch],
        )
    )

    story.append(para("Models Used", styles, "Section"))
    story.extend(
        bullet_items(
            [
                "TF-IDF baseline for quick and lightweight text matching.",
                "Cosine similarity for resume and job description comparison.",
                "Sentence Transformers such as all-MiniLM-L6-v2 for advanced semantic matching.",
                "Optional classifier models such as Logistic Regression, Random Forest, or XGBoost for shortlist/reject classification.",
            ],
            styles,
        )
    )

    story.append(para("Implementation Modules", styles, "Section"))
    story.append(
        table(
            [
                ["File", "Purpose"],
                ["app.py", "Main Streamlit application and user interface."],
                ["src/parser.py", "Extracts resume text from supported document formats."],
                ["src/preprocess.py", "Cleans and normalizes text before matching."],
                ["src/vectorizer.py", "Generates TF-IDF vectors or transformer embeddings."],
                ["src/matcher.py", "Computes cosine similarity scores."],
                ["src/ranker.py", "Ranks candidates and assigns shortlist status."],
                ["src/skill_extractor.py", "Extracts matched and missing skills."],
                ["utils/helpers.py", "Provides helper functions for uploaded files and display formatting."],
            ],
            [1.8 * inch, 4.5 * inch],
        )
    )

    story.append(para("Application Workflow", styles, "Section"))
    story.extend(
        bullet_items(
            [
                "The user uploads one or more resumes through the Streamlit interface.",
                "The user enters the job description in the input box.",
                "The parser converts each resume into plain text.",
                "The preprocessing module cleans resume and job description text.",
                "The vectorizer converts text into TF-IDF vectors or semantic embeddings.",
                "The matcher calculates cosine similarity scores.",
                "The ranker sorts candidates and marks each as Shortlist or Review.",
                "The UI displays a ranked table and match score visualization.",
            ],
            styles,
        )
    )
    story.append(PageBreak())

    story.append(para("Example Output", styles, "Section"))
    story.append(
        table(
            [
                ["Rank", "Candidate", "Match Score", "Status", "Extracted Skills", "Missing Skills"],
                ["1", "resume_01.pdf", "87%", "Shortlist", "Python, SQL, Machine Learning", "Docker"],
                ["2", "resume_02.pdf", "64%", "Review", "Python, Streamlit", "SQL, AWS"],
            ],
            [0.45 * inch, 1.1 * inch, 0.85 * inch, 0.8 * inch, 1.8 * inch, 1.3 * inch],
        )
    )

    story.append(para("Testing", styles, "Section"))
    story.append(
        para(
            "The project includes automated tests for preprocessing and ranking behavior. A manual smoke test was also performed for the TF-IDF ranking pipeline. The sample test confirmed that a resume containing Python, SQL, and machine learning skills ranks higher than an unrelated resume and receives Shortlist status when it passes the threshold.",
            styles,
        )
    )
    story.append(
        table(
            [
                ["Test Area", "Result"],
                ["Syntax compilation", "Passed"],
                ["Unit tests", "Passed"],
                ["Dependency imports", "Passed for core dependencies"],
                ["TF-IDF ranking pipeline", "Passed"],
                ["Streamlit web endpoint", "Responded successfully"],
            ],
            [2.0 * inch, 4.3 * inch],
        )
    )

    story.append(para("Advantages", styles, "Section"))
    story.extend(
        bullet_items(
            [
                "Reduces manual resume screening effort.",
                "Provides consistent ranking criteria.",
                "Highlights matched and missing skills.",
                "Supports both baseline and advanced semantic matching.",
                "Can be extended with explainability and deployment features.",
            ],
            styles,
        )
    )

    story.append(para("Limitations", styles, "Section"))
    story.extend(
        bullet_items(
            [
                "Accuracy depends on the quality of resume text extraction.",
                "Skill extraction uses a predefined skill dictionary in the current version.",
                "Sentence Transformer mode requires additional dependencies and model availability.",
                "The system should be audited for bias before real-world hiring use.",
            ],
            styles,
        )
    )

    story.append(para("Future Improvements", styles, "Section"))
    story.extend(
        bullet_items(
            [
                "Add recruiter feedback loop to improve ranking quality.",
                "Improve extracted skills using named entity recognition.",
                "Generate LLM-based candidate explanations.",
                "Add bias detection and fairness monitoring.",
                "Deploy the application online.",
                "Add candidate comparison and analytics dashboard.",
            ],
            styles,
        )
    )

    story.append(para("Conclusion", styles, "Section"))
    story.append(
        para(
            "The AI-Based Resume Screening System demonstrates how NLP and Machine Learning can simplify candidate screening. By combining resume parsing, preprocessing, vectorization, cosine similarity, ranking, and a Streamlit interface, the project provides an efficient and practical solution for shortlisting candidates according to job relevance.",
            styles,
        )
    )

    story.append(para("References", styles, "Section"))
    story.extend(
        bullet_items(
            [
                "scikit-learn documentation for TF-IDF and cosine similarity.",
                "Sentence Transformers documentation for semantic embeddings.",
                "Streamlit documentation for web application development.",
                "pdfplumber, PyMuPDF, and python-docx documentation for document parsing.",
                "O*NET and ESCO skill taxonomies for future skill database expansion.",
            ],
            styles,
        )
    )

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.7 * inch,
        title="AI-Based Resume Screening System Report",
        author="Codex",
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    build_report()
    print(OUTPUT)

# AI-Based Resume Screening System

## Description

An intelligent resume screening system using Natural Language Processing and Machine Learning to automatically rank job candidates based on skill match, relevance, and similarity with the job description.

The system accepts multiple resumes, extracts text from them, preprocesses the content, generates feature vectors or embeddings, calculates similarity scores, ranks candidates, and displays the results through a Streamlit web interface.

## Features

- Resume parsing
- Skill extraction
- Semantic matching
- Ranking engine
- Candidate shortlisting
- Web interface using Streamlit
- Explainable AI support
- Match score visualization
- Missing skill identification

## Tech Stack

- Python
- NLP: spaCy, NLTK
- Machine Learning: scikit-learn
- Transformers: Sentence Transformers
- Streamlit
- Pandas
- NumPy
- PDF/DOCX parsing: pdfplumber, PyMuPDF, python-docx

## Workflow

1. Resume upload
2. Job description input
3. Resume parsing
4. Text preprocessing
5. Embedding generation
6. Similarity scoring
7. Ranking and shortlisting
8. Results visualization

## Architecture

```text
Resume Upload / Job Description
        |
Document Parsing
        |
NLP Preprocessing
        |
Feature Engineering / Embeddings
        |
Similarity Computation
        |
Ranking Engine
        |
Results Visualization
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Optional advanced NLP and transformer dependencies:

```bash
pip install -r requirements-advanced.txt
```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Models Used

- TF-IDF baseline
- Cosine similarity
- Sentence Transformers

Recommended Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

Use `TF-IDF baseline` for quick local testing. Use `Sentence Transformer` for stronger semantic matching after installing `requirements-advanced.txt`.

## Example Output

The system displays a ranked table containing:

- Rank
- Candidate or resume file name
- Match score
- Shortlist status
- Extracted skills
- Missing skills

Example:

| Rank | Candidate | Match Score | Status | Extracted Skills | Missing Skills |
|---|---|---:|---|---|---|
| 1 | resume_01.pdf | 87% | Shortlist | Python, SQL, Machine Learning | Docker |
| 2 | resume_02.pdf | 64% | Review | Python, Streamlit | SQL, AWS |

## Project Structure

```text
AI_Resume_Screening/
|
+-- data/
|   +-- resumes/
|   +-- job_descriptions/
|
+-- models/
|   +-- embedding_model/
|
+-- src/
|   +-- parser.py
|   +-- preprocess.py
|   +-- vectorizer.py
|   +-- matcher.py
|   +-- ranker.py
|   +-- skill_extractor.py
|
+-- utils/
|   +-- helpers.py
|
+-- tests/
+-- app.py
+-- requirements.txt
+-- requirements-advanced.txt
+-- README.md
```

## Core Modules

- `src/parser.py`: Extracts plain text from PDF, DOCX, DOC, and TXT files
- `src/preprocess.py`: Cleans and normalizes resume and job description text
- `src/vectorizer.py`: Generates TF-IDF vectors or transformer embeddings
- `src/matcher.py`: Computes cosine similarity scores
- `src/ranker.py`: Sorts resumes and assigns shortlist status
- `src/skill_extractor.py`: Finds matched and missing skills
- `app.py`: Main Streamlit web application

## Dataset Suggestions

Search Kaggle for:

- Resume Dataset
- Recruitment Dataset
- CV/Resume Text Dataset
- Resume NER Dataset
- Job Description Dataset

Skill taxonomies:

- O*NET Skills Database
- ESCO Skill Taxonomy
- Public GitHub skill lists

## Future Improvements

- Feedback loop for improving recommendations
- Better extracted skills using named entity recognition
- LLM-generated candidate explanations
- Bias detection
- Online deployment
- Recruiter feedback dashboard
- Candidate comparison view

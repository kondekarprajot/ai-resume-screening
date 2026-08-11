# AI Based Resume Screening System

This project screens multiple resumes against a job description using resume parsing, NLP preprocessing, feature representation, cosine similarity, ranking, and a Streamlit web interface.

## Features

- Upload multiple resumes in PDF, DOC, DOCX, or TXT format
- Paste a job description
- Extract text from uploaded documents
- Preprocess text with lowercasing, special character cleanup, stop word removal, lemmatization fallback, and skill normalization
- Match resumes using TF-IDF cosine similarity or Sentence Transformer embeddings
- Rank candidates by match percentage
- Show matched skills, missing skills, and shortlist status
- Visualize match percentages in the web UI

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

## Folder Structure

```text
AI_Resume_Screening/
|
├── data/
│   ├── resumes/
│   └── job_descriptions/
|
├── models/
│   └── embedding_model/
|
├── src/
│   ├── parser.py
│   ├── preprocess.py
│   ├── vectorizer.py
│   ├── matcher.py
│   ├── ranker.py
│   └── skill_extractor.py
|
├── utils/
│   └── helpers.py
|
├── tests/
├── app.py
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Optional advanced NLP and transformer dependencies:

```bash
pip install -r requirements-advanced.txt
```

Run the app:

```bash
streamlit run app.py
```

## Recommended Usage

Use `TF-IDF baseline` for quick local testing. Use `Sentence Transformer` for stronger semantic matching after installing `requirements-advanced.txt` and when the model is already cached or the machine has internet access for first-time model download.

The default advanced model is:

```text
all-MiniLM-L6-v2
```

## Core Modules

- `src/parser.py`: Extracts plain text from PDF, DOCX, DOC, and TXT files
- `src/preprocess.py`: Cleans and normalizes text
- `src/vectorizer.py`: Generates TF-IDF vectors or transformer embeddings
- `src/matcher.py`: Computes cosine similarity scores
- `src/ranker.py`: Sorts resumes and assigns shortlist status
- `src/skill_extractor.py`: Finds matched and missing skills
- `app.py`: Streamlit web application

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

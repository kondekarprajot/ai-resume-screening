from __future__ import annotations

import pandas as pd
import streamlit as st

from src.matcher import compute_similarity_scores
from src.parser import SUPPORTED_EXTENSIONS, extract_text
from src.preprocess import preprocess_text
from src.ranker import rank_resumes
from src.skill_extractor import compare_skills
from src.vectorizer import TextVectorizer
from utils.helpers import comma_join, save_temp_upload


st.set_page_config(page_title="AI Resume Screening", layout="wide")


def main() -> None:
    st.title("AI Based Resume Screening System")

    with st.sidebar:
        st.header("Screening Settings")
        model_mode = st.selectbox(
            "Matching model",
            ["tfidf", "sentence-transformer"],
            format_func=lambda value: "TF-IDF baseline"
            if value == "tfidf"
            else "Sentence Transformer",
        )
        threshold = st.slider("Shortlist threshold", 0, 100, 60)
        model_name = st.text_input("Transformer model", "all-MiniLM-L6-v2")

    resumes = st.file_uploader(
        "Upload resumes",
        type=[extension.lstrip(".") for extension in SUPPORTED_EXTENSIONS],
        accept_multiple_files=True,
    )
    job_description = st.text_area("Job description", height=220)

    if st.button("Rank Resumes", type="primary"):
        if not resumes:
            st.warning("Upload at least one resume.")
            return
        if not job_description.strip():
            st.warning("Enter a job description.")
            return

        with st.spinner("Parsing and ranking resumes..."):
            results = screen_resumes(resumes, job_description, model_mode, model_name, threshold)

        st.subheader("Ranked Results")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Rank": index,
                        "Resume": result.file_name,
                        "Match %": result.match_percentage,
                        "Status": result.status,
                        "Top skills found": comma_join(result.matched_skills),
                        "Missing skills": comma_join(result.missing_skills),
                    }
                    for index, result in enumerate(results, start=1)
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.bar_chart(
            pd.DataFrame(
                {
                    "Resume": [result.file_name for result in results],
                    "Match %": [result.match_percentage for result in results],
                }
            ).set_index("Resume")
        )


def screen_resumes(uploaded_files, job_description, model_mode, model_name, threshold):
    file_names = []
    resume_texts = []
    processed_resumes = []
    matched_skills = []
    missing_skills = []

    processed_jd = preprocess_text(job_description)

    for uploaded_file in uploaded_files:
        path = save_temp_upload(uploaded_file)
        text = extract_text(path)
        file_names.append(uploaded_file.name)
        resume_texts.append(text)
        processed_resumes.append(preprocess_text(text))
        matched, missing = compare_skills(text, job_description)
        matched_skills.append(matched)
        missing_skills.append(missing)

    vectorizer = TextVectorizer(mode=model_mode, model_name=model_name)
    vectors = vectorizer.vectorize(processed_resumes + [processed_jd])
    resume_vectors = vectors[:-1]
    jd_vector = vectors[-1]
    scores = compute_similarity_scores(resume_vectors, jd_vector)

    return rank_resumes(file_names, scores, matched_skills, missing_skills, threshold)


if __name__ == "__main__":
    main()

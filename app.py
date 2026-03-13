import streamlit as st
import fitz
import re
import ollama
import spacy
from sentence_transformers import SentenceTransformer
import joblib
from sqlalchemy import create_engine, text

nlp = spacy.load("en_core_web_sm")

sbert_model = SentenceTransformer('sbert_model')
rf_model = joblib.load('rf_model.joblib')

llm_model = "llama3.2:1b"

def get_engine():
    username = ""
    password = ""
    host = ""
    port = ""
    database = "candidate_resumes"

    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")
    return engine


def extract_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    doc = nlp(text)
    cleaned_text = " ".join([token.lemma_ for token in doc if not token.is_stop])
    return cleaned_text


def classify_job_desc(job_desc):
    emb = sbert_model.encode([job_desc])
    role = rf_model.predict(emb)[0]
    return role


def calculate_similarity(job_desc, resume_text):
    prompt = (
        f"Compare the following job description and resume.\n\n"
        f"Job Description: {job_desc}\n\n"
        f"Resume: {resume_text}\n\n"
        f"Provide a similarity score from 0 to 100 and explain why."
    )

    response = ollama.chat(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response["message"]["content"]

    match = re.search(r'\b(\d{1,3})\b', response_text)
    if match:
        score = int(match.group(1))
        if score > 100:
            score = 100
        return score / 100
    return 0


def store_in_database(role, top_resumes):
    engine = get_engine()

    with engine.begin() as connection:
        for resume_name, score in top_resumes:
            query = text(
                "INSERT INTO top_matches (role, resume_name, score) VALUES (:role, :resume_name, :score)"
            )
            connection.execute(query, {
                "role": role,
                "resume_name": resume_name,
                "score": score
            })

    engine.dispose()


st.title("AI-Powered Resume Matching and Shortlisting System")
st.write("Upload a Job Description and Resumes to find the best matches.")

job_desc = st.text_area("Enter Job Description", "")
uploaded_files = st.file_uploader("Upload Resumes in PDF format", type=["pdf"], accept_multiple_files=True)

if st.button("Match Resumes"):
    if job_desc and uploaded_files:
        job_desc_cleaned = preprocess_text(job_desc)
        role = classify_job_desc(job_desc_cleaned)

        st.write(f"Job Role is classified as: {role}")

        resume_scores = []

        for resume_file in uploaded_files:
            resume_text = extract_text(resume_file)
            resume_text_cleaned = preprocess_text(resume_text)

            similarity_score = calculate_similarity(
                job_desc_cleaned,
                resume_text_cleaned
            )

            resume_scores.append((resume_file.name, similarity_score))

        resume_scores.sort(key=lambda x: x[1], reverse=True)

        st.subheader("Top Resume Matches for this Job Description")

        for resume_name, score in resume_scores[:5]:
            st.write(f"**{resume_name}**: {float(score) * 100:.2f}%")

        store_in_database(role, resume_scores[:5])
        st.success("Top matches have been stored in the database.")

    else:
        st.warning("Please enter a Job Description and upload at least one Resume.")

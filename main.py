import streamlit as st
import fitz
import re
import ollama
import spacy
import mysql.connector

# Load Spacy NLP Model
nlp = spacy.load("en_core_web_sm")

# Define Ollama model
model_name = "llama3.2:1b"

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

def calculate_similarity(job_desc, resume_text):
    prompt = (
        f"Compare the following job description and resume.\n\n"
        f"Job Description: {job_desc}\n\n"
        f"Resume: {resume_text}\n\n"
        f"Provide a similarity score from 0 to 100 and explain why."
    )
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    
    # Extract similarity score from response (assumes score is mentioned in response)
    match = re.search(r'(\d+)', response["message"]["content"])
    if match:
        return int(match.group(1)) / 100  # Convert to decimal (0 to 1 scale)
    return 0  # Default if no match found

def store_in_database(job_desc, top_resumes):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="top_resumes_db"
    )
    cursor = conn.cursor()
    
    for resume_name, score in top_resumes:
        query = "INSERT INTO matches (job_desc, resume_name, score) VALUES (%s, %s, %s)"
        values = (job_desc, resume_name, score)
        cursor.execute(query, values)
    
    conn.commit()
    cursor.close()
    conn.close()

st.title("AI-Powered Resume Matching and Shortlisting System")
st.write("Upload a Job Description and Resumes to find the best matches.")

job_desc = st.text_area("Enter Job Description", "")
uploaded_files = st.file_uploader("Upload Resumes in PDF format", type=["pdf"], accept_multiple_files=True)

if st.button("Match Resumes"):
    if job_desc and uploaded_files:
        job_desc_cleaned = preprocess_text(job_desc)
        resume_scores = []

        for resume_file in uploaded_files:
            resume_text = extract_text(resume_file)
            resume_text_cleaned = preprocess_text(resume_text)
            similarity_score = calculate_similarity(job_desc_cleaned, resume_text_cleaned)
            resume_scores.append((resume_file.name, similarity_score))

        resume_scores.sort(key=lambda x: x[1], reverse=True)

        st.subheader("Top Resume Matches for this Job Description")
        for resume_name, score in resume_scores[:5]:
            st.write(f"**{resume_name}** - Matching Score: {score * 100:.2f}%")

        store_in_database(job_desc, resume_scores[:5])
    else:
        st.warning("Please enter a Job Description and upload at least one Resume.")

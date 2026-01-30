# 🤖 AI-powered Resume Matching and Shortlisting System

An intelligent AI Agent that analyzes multiple candidate resumes and compares them with a given Job Description (JD) to automatically **shortlist the top 5 most relevant candidates**. The system enhances recruitment efficiency by reducing manual screening, improving accuracy, and promoting fairness in candidate-job matching.

## 🚀 Features
- **spaCy**: Loads a small NLP English language model 
- **Llama3.2:1b**: Analyzes resumes with the JD for top results
- **XAMPP MySQL**: Stores the top resumes in database
- **Streamlit**: Interactive dashboard

## 📄 Workflow

- User uploads multiple candidate resumes
- User inputs a job description (JD) from the recruiter
- NLP model and other techniques pre-process the resumes for smooth analysis
- Llama3.2:1b compares the resumes with the given JD
- Automatically shortlists and displays the top 5 best-suiting resumes with matching scores
- Stores shortlisted resumes and match scores in the database

## 🧰 Tech Stack

- **Frontend:** Streamlit
- **NLP:** spaCy
- **LLM:** Llama 3.2:1b (via Ollama)
- **Database:** XAMPP (MySQL)

## 📢 Future Enhancements

- Add support for ranking beyond top 5
- Incorporate interview scheduling suggestions
- Export shortlists as CSV or PDF
- Add job role classification from JD

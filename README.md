# 🤖 AI-powered Resume Matching and Shortlisting System

An intelligent AI Agent that analyzes multiple candidate resumes and compares them with a given Job Description (JD) to automatically **shortlist the top 5 most relevant candidates**. The system enhances recruitment efficiency by reducing manual screening, improving accuracy, and promoting fairness in candidate-job matching.

## 🚀 Features
- **spaCy**: Loads a small NLP English language model
- **Sentence BERT and Random Forest Classifier**: Analyze the Job Description 
- **Llama3.2:1b**: Analyzes resumes with the JD 
- **MySQL**: Stores the top resumes in database
- **Streamlit**: Interactive dashboard

## 📄 Workflow

- User uploads multiple candidate resumes
- User inputs a job description (JD) from the recruiter
- Sentence BERT and Random Forest Classifier Models analyze the Job Description and classify the Job Title
- NLP model and other techniques pre-process the resumes for smooth analysis
- Llama3.2:1b compares the resumes with the given JD
- Automatically shortlists and displays the top 5 best-suiting resumes with matching scores
- Stores shortlisted resumes and match scores with the classified job title in the database

## 🧰 Tech Stack

- **Frontend:** Streamlit
- **NLP:** spaCy
- **Model:s** Sentence BERT, Random Forest Classifier
- **LLM:** Llama 3.2:1b (via Ollama)
- **Database:** MySQL

## 📢 Future Enhancements

- Export shortlists as CSV or PDF
- Incorporate interview scheduling suggestions

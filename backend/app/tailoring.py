
import spacy
from app.utils import call_gpt

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    return [chunk.text for chunk in doc.noun_chunks]

def process_resume(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    matched_skills = set(resume_keywords) & set(job_keywords)
    missing_skills = set(job_keywords) - set(resume_keywords)

    suggestions = call_gpt(f"""
Given the following resume:\n{resume_text}\n
and this job description:\n{job_description}\n
- Highlight matched skills: {list(matched_skills)}
- Suggest tailored bullet points focusing on the missing skills: {list(missing_skills)}
- Rewrite the summary to better fit the job.
""")

    return {
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "suggestions": suggestions
    }

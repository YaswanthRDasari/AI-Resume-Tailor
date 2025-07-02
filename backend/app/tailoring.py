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

    tailored_latex = call_gpt(f"""
Given the following LaTeX resume content:
{resume_text}

and this job description:
{job_description}

- Instructions:
- ONLY edit the content inside the document (between \\begin{{document}} and \\end{{document}}).
- DO NOT change the preamble (everything before \\begin{{document}}).
- Rephrase and align the resume content (summaries, skills, experiences, etc.) to closely match the job description, but ONLY using the skills and experiences already present in the resume.
- Do NOT add any new skills or experiences that are not in the resume.
- If a skills section is missing, create one from the skills already present in the resume.
- ENSURE the output is valid, compilable LaTeX with no syntax errors (all environments and braces must match, all commands must be valid).
- Return the full LaTeX file, ready to compile, preserving all formatting, sections, and structure.
- Do NOT add any stray numbers, units, or LaTeX commands (such as '1em 1em 1em 0pt 6pt \\\\') that are not part of the original or required sections.
- Only use valid LaTeX commands and content relevant to a professional resume.
""")

    return {
        "matched_skills": list(matched_skills),
        "latex_content": tailored_latex,
        "latex_filename": "tailored_resume.tex"
    }

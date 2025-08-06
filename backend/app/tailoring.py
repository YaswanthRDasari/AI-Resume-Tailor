# import spacy
# from app.utils import call_gpt

# nlp = spacy.load("en_core_web_sm")

# def extract_keywords(text):
#     doc = nlp(text)
#     return [chunk.text for chunk in doc.noun_chunks]

# def process_resume(resume_text, job_description):
#     resume_keywords = extract_keywords(resume_text)
#     job_keywords = extract_keywords(job_description)

#     matched_skills = set(resume_keywords) & set(job_keywords)

#     tailored_latex = call_gpt(f"""
# Given the following LaTeX resume content:
# {resume_text}

# and this job description:
# {job_description}

# - Instructions:
# - ONLY edit the content inside the document (between \\begin{{document}} and \\end{{document}}).
# - DO NOT change the preamble (everything before \\begin{{document}}).
# - Rephrase and align the resume content (summaries, skills, experiences, etc.) to closely match the job description, but ONLY using the skills and experiences already present in the resume.
# - Do NOT add any new skills or experiences that are not in the resume.
# - If a skills section is missing, create one from the skills already present in the resume.
# - ENSURE the output is valid, compilable LaTeX with no syntax errors (all environments and braces must match, all commands must be valid).
# - Return the full LaTeX file, ready to compile, preserving all formatting, sections, and structure.
# - Do NOT add any stray numbers, units, or LaTeX commands (such as '1em 1em 1em 0pt 6pt \\\\') that are not part of the original or required sections.
# - Only use valid LaTeX commands and content relevant to a professional resume.
# """)

#     return {
#         "matched_skills": list(matched_skills),
#         "latex_content": tailored_latex,
#         "latex_filename": "tailored_resume.tex"
#     }



import spacy
from app.utils import call_gpt
import re
from typing import Dict, List, Tuple

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text: str) -> List[str]:
    """Extracts noun chunks as keywords from a given text."""
    doc = nlp(text)
    return [chunk.text for chunk in doc.noun_chunks]

def anonymize_text(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Finds PII (persons, organizations) and replaces them with placeholders.
    Returns the anonymized text and a map for de-anonymization.
    """
    doc = nlp(text)
    anonymized_text = text
    anonymization_map = {}
    
    # Use sets to get unique entities and then sort for consistent ordering
    persons = sorted(list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"])))
    orgs = sorted(list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"])))

    for i, person in enumerate(persons):
        placeholder = f"[PERSON_{i+1}]"
        # Use regex for whole-word replacement to avoid replacing parts of words
        anonymized_text = re.sub(r'\b' + re.escape(person) + r'\b', placeholder, anonymized_text)
        anonymization_map[placeholder] = person

    for i, org in enumerate(orgs):
        placeholder = f"[ORG_{i+1}]"
        anonymized_text = re.sub(r'\b' + re.escape(org) + r'\b', placeholder, anonymized_text)
        anonymization_map[placeholder] = org

    return anonymized_text, anonymization_map

def de_anonymize_text(text: str, anonymization_map: Dict[str, str]) -> str:
    """
    Replaces placeholders in the text with their original PII values.
    """
    for placeholder, original_text in anonymization_map.items():
        text = text.replace(placeholder, original_text)
    return text

def process_resume(resume_text: str, job_description: str):
    """
    Anonymizes resume, tailors it using AI, and then de-anonymizes the result.
    """
    try:
        print(f"[DEBUG] Starting process_resume with resume length: {len(resume_text)}")
        
        # 1. Anonymize the resume text to protect PII
        anonymized_resume, anonymization_map = anonymize_text(resume_text)
        print(f"[DEBUG] Anonymized resume length: {len(anonymized_resume)}")
        
        # Extract keywords for skill analysis
        resume_keywords_set = set(extract_keywords(resume_text))
        job_keywords_set = set(extract_keywords(job_description))
        
        print(f"[DEBUG] Resume keywords count: {len(resume_keywords_set)}")
        print(f"[DEBUG] Job keywords count: {len(job_keywords_set)}")

        matched_skills = list(resume_keywords_set & job_keywords_set)
        missing_skills = list(job_keywords_set - resume_keywords_set)
        
        print(f"[DEBUG] Matched skills: {matched_skills}")
        print(f"[DEBUG] Missing skills: {missing_skills}")
        
        # 2. Update the prompt to instruct the AI to preserve placeholders
        prompt = f"""
Given the following anonymized LaTeX resume content:
{anonymized_resume}

and this job description:
{job_description}

- Instructions:
- **IMPORTANT**: Preserve all placeholders like `[PERSON_1]` and `[ORG_1]` exactly as they are. Do NOT modify or translate them.
- ONLY edit the content inside the document (between \\begin{{document}} and \\end{{document}}).
- DO NOT change the preamble (everything before \\begin{{document}}).
- Rephrase and align the resume content (summaries, skills, experiences, etc.) to closely match the job description, but ONLY using the skills and experiences already present in the resume.
- Do NOT add any new skills or experiences that are not in the resume.
- If a skills section is missing, create one from the skills already present in the resume.
- ENSURE the output is valid, compilable LaTeX with no syntax errors.
- Return the full LaTeX file, ready to compile, preserving all formatting, sections, and structure.
- Only use valid LaTeX commands and content relevant to a professional resume.
"""

        print(f"[DEBUG] Calling GPT with prompt length: {len(prompt)}")
        anonymized_latex_result = call_gpt(prompt)
        print(f"[DEBUG] GPT response length: {len(anonymized_latex_result) if anonymized_latex_result else 0}")

        # 3. De-anonymize the AI's response to restore the original PII
        tailored_latex = de_anonymize_text(anonymized_latex_result, anonymization_map)
        print(f"[DEBUG] Final tailored latex length: {len(tailored_latex)}")

        result = {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "latex_content": tailored_latex,
            "latex_filename": "tailored_resume.tex"
        }
        
        print(f"[DEBUG] Returning result with keys: {list(result.keys())}")
        return result
        
    except Exception as e:
        print(f"[ERROR] Exception in process_resume: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "error": f"Processing failed: {str(e)}",
            "matched_skills": [],
            "missing_skills": [],
            "latex_content": "",
            "latex_filename": "error.tex"
        }

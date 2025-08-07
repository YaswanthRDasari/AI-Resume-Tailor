import spacy
from app.utils import call_gpt
import re
from typing import Dict, List, Tuple
import math

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_experience_years(text: str) -> int:
    """Extract years of experience from text using GPT and date analysis"""
    
    # First, try to calculate from date ranges (more accurate)
    print("[DEBUG] Attempting to calculate experience from date ranges...")
    date_calculated_years = calculate_experience_from_dates(text)
    
    if date_calculated_years > 0:
        print(f"[DEBUG] Successfully calculated {date_calculated_years} years from dates")
        return round(date_calculated_years)
    
    # Fallback to GPT extraction
    print("[DEBUG] Falling back to GPT extraction...")
    prompt = f"""
Extract the total years of PROFESSIONAL experience from the following text.
IMPORTANT: 
- Return ONLY a single number representing total years of experience (e.g., 5, 3, 7).
- Do NOT include internships, part-time work, or academic projects in the total.
- Only count full-time professional work experience.
- If multiple roles, sum only the professional experience years.
- Do NOT include any other numbers like calendar years (2020, 2023, etc.) or other text.
- If no specific years mentioned, estimate based on job history and roles.

Text: {text}
"""
    
    try:
        response = call_gpt(prompt)
        print(f"[DEBUG] GPT experience response: {response}")
        
        # Clean the response and extract only experience years
        cleaned_response = response.strip().lower()
        
        # Look for patterns like "X years", "X year", "X yrs", etc.
        # Prioritize professional experience patterns
        year_patterns = [
            # Professional experience patterns (highest priority)
            r'(\d+)\s*years?\s*of\s*professional\s*experience',
            r'(\d+)\s*yrs?\s*of\s*professional\s*experience',
            r'(\d+)\s*years?\s*professional\s*experience',
            r'(\d+)\s*yrs?\s*professional\s*experience',
            
            # General experience patterns (medium priority)
            r'(\d+)\s*years?\s*of\s*experience',
            r'(\d+)\s*yrs?\s*of\s*experience', 
            r'(\d+)\s*years?\s*experience',
            r'(\d+)\s*yrs?\s*experience',
            
            # Simple patterns (lowest priority)
            r'(\d+)\s*years?',
            r'(\d+)\s*yrs?',
            r'^(\d+)$'  # Just a number
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, cleaned_response)
            if match:
                years = int(match.group(1))
                # Sanity check: reasonable experience range (0-50 years)
                if 0 <= years <= 50:
                    print(f"[DEBUG] Extracted {years} years of experience")
                    return years
                else:
                    print(f"[WARNING] Unreasonable years extracted: {years}, skipping")
        
        # Fallback: extract any reasonable number
        numbers = re.findall(r'\d+', cleaned_response)
        for num_str in numbers:
            years = int(num_str)
            if 0 <= years <= 50:
                print(f"[DEBUG] Fallback extracted {years} years of experience")
                return years
        
        print(f"[WARNING] No reasonable years found in response: {response}")
        return 0
        
    except Exception as e:
        print(f"[ERROR] Failed to extract experience years: {str(e)}")
        return 0

def calculate_experience_from_dates(text: str) -> float:
    """Calculate experience from date ranges in the text"""
    try:
        # Look for date patterns like "2020-2023", "2018-2020", etc.
        date_patterns = [
            r'(\d{4})\s*-\s*(\d{4})',  # 2020-2023
            r'(\d{4})\s*to\s*(\d{4})',  # 2020 to 2023
            r'(\d{4})\s*until\s*(\d{4})',  # 2020 until 2023
            r'(\d{4})\s*-\s*present',  # 2020-Present
            r'(\d{4})\s*to\s*present',  # 2020 to Present
            r'(\d{4})\s*-\s*now',  # 2020-Now
        ]
        
        total_years = 0.0
        professional_roles = 0
        
        # Split text into lines to analyze each role separately
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            
            # Skip lines that mention internships, part-time, or academic work
            if any(keyword in line_lower for keyword in ['internship', 'intern', 'part-time', 'academic', 'student', 'research assistant']):
                continue
                
            # Look for date ranges in this line
            for pattern in date_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    if len(match) == 2:  # Regular date range
                        start_year, end_year = match
                        start = int(start_year)
                        
                        # Handle "Present" dates
                        if end_year.lower() in ['present', 'now', 'current']:
                            from datetime import datetime
                            current_year = datetime.now().year
                            end = current_year
                        else:
                            end = int(end_year)
                        
                        # Sanity check for reasonable years
                        if 1990 <= start <= 2030 and 1990 <= end <= 2030 and start <= end:
                            years = end - start
                            
                            # Check if this looks like a professional role
                            professional_keywords = ['engineer', 'developer', 'manager', 'analyst', 'consultant', 'specialist', 'lead', 'senior', 'junior']
                            if any(keyword in line_lower for keyword in professional_keywords):
                                total_years += years
                                professional_roles += 1
                                print(f"[DEBUG] Found professional role: {start}-{end} ({years} years)")
                    elif len(match) == 1:  # Single year (like "2020-Present")
                        start_year = match[0]
                        start = int(start_year)
                        
                        # Handle "Present" dates
                        from datetime import datetime
                        current_year = datetime.now().year
                        end = current_year
                        
                        # Sanity check for reasonable years
                        if 1990 <= start <= 2030 and 1990 <= end <= 2030 and start <= end:
                            years = end - start
                            
                            # Check if this looks like a professional role
                            professional_keywords = ['engineer', 'developer', 'manager', 'analyst', 'consultant', 'specialist', 'lead', 'senior', 'junior']
                            if any(keyword in line_lower for keyword in professional_keywords):
                                total_years += years
                                professional_roles += 1
                                print(f"[DEBUG] Found professional role: {start}-{end} ({years} years)")
        
        if professional_roles > 0:
            print(f"[DEBUG] Calculated {total_years} years from {professional_roles} professional roles")
            return total_years
        
        return 0.0
        
    except Exception as e:
        print(f"[ERROR] Failed to calculate experience from dates: {str(e)}")
        return 0.0

def extract_job_requirements(text: str) -> Dict[str, any]:
    """Extract job requirements and their importance from job description"""
    prompt = f"""
Analyze this job description and extract key requirements with their importance levels.

Return ONLY a JSON object with this structure:
{{
    "required_years": number (only years of experience required, not calendar years),
    "required_skills": ["skill1", "skill2"],
    "preferred_skills": ["skill1", "skill2"],
    "required_education": "degree level",
    "experience_level": "entry/mid/senior/lead",
    "industry": "tech/finance/healthcare/etc"
}}

IMPORTANT: For "required_years", extract only the number of years of experience required (e.g., 5, 3, 7).
Do NOT include calendar years like 2020, 2023, etc.

Job Description: {text}
"""
    
    try:
        response = call_gpt(prompt)
        # Try to extract JSON from response
        import json
        # Find JSON-like content in response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {}
    except Exception as e:
        print(f"[ERROR] Failed to extract job requirements: {str(e)}")
        return {}

def calculate_skill_match_score(resume_skills: List[str], job_skills: List[str], 
                              required_skills: List[str], preferred_skills: List[str]) -> float:
    """Calculate skill match score based on required vs preferred skills"""
    if not job_skills:
        return 0.0
    
    resume_skills_lower = [skill.lower() for skill in resume_skills]
    required_skills_lower = [skill.lower() for skill in required_skills]
    preferred_skills_lower = [skill.lower() for skill in preferred_skills]
    
    # Calculate required skills match (weighted higher)
    required_matches = sum(1 for skill in required_skills_lower if skill in resume_skills_lower)
    required_score = (required_matches / len(required_skills_lower)) * 0.7 if required_skills_lower else 0.0
    
    # Calculate preferred skills match (weighted lower)
    preferred_matches = sum(1 for skill in preferred_skills_lower if skill in resume_skills_lower)
    preferred_score = (preferred_matches / len(preferred_skills_lower)) * 0.3 if preferred_skills_lower else 0.0
    
    return required_score + preferred_score

def calculate_experience_score(resume_years: int, required_years: int) -> float:
    """Calculate experience match score"""
    if required_years == 0:
        return 0.8  # Default score if no requirement specified
    
    if resume_years >= required_years:
        # Bonus for exceeding requirements (up to 50% more)
        excess = min(resume_years - required_years, required_years * 0.5)
        return 0.8 + (excess / required_years) * 0.2
    else:
        # Penalty for insufficient experience
        return max(0.0, 0.8 - ((required_years - resume_years) / required_years) * 0.8)

def get_recommendation_level(overall_score: float) -> Tuple[str, str, str]:
    """Get recommendation level based on overall score"""
    if overall_score >= 0.85:
        return "Strongly Recommended", "Excellent match! This position aligns very well with your background.", "green"
    elif overall_score >= 0.70:
        return "Recommended", "Good match. You have most of the required qualifications.", "blue"
    elif overall_score >= 0.50:
        return "Consider Applying", "Moderate match. Some gaps exist but worth applying.", "orange"
    elif overall_score >= 0.30:
        return "Weak Match", "Limited alignment. Consider improving your profile first.", "yellow"
    else:
        return "Not Recommended", "Poor match. This position doesn't align with your background.", "red"

def calculate_match_score(resume_text: str, job_description: str, 
                         resume_skills: List[str], job_skills: List[str]) -> Dict[str, any]:
    """Calculate comprehensive match score and recommendation"""
    
    # Extract experience years
    resume_years = extract_experience_years(resume_text)
    
    # Extract job requirements
    job_requirements = extract_job_requirements(job_description)
    required_years = job_requirements.get('required_years', 0)
    required_skills = job_requirements.get('required_skills', [])
    preferred_skills = job_requirements.get('preferred_skills', [])
    experience_level = job_requirements.get('experience_level', 'mid')
    industry = job_requirements.get('industry', 'tech')
    
    # Calculate individual scores
    skill_score = calculate_skill_match_score(resume_skills, job_skills, required_skills, preferred_skills)
    experience_score = calculate_experience_score(resume_years, required_years)
    
    # Calculate overall score (weighted average)
    overall_score = (skill_score * 0.6) + (experience_score * 0.4)
    
    # Get recommendation
    recommendation_level, recommendation_text, color = get_recommendation_level(overall_score)
    
    # Calculate detailed breakdown
    skill_match_percentage = skill_score * 100
    experience_match_percentage = experience_score * 100
    
    # Identify gaps
    missing_required = [skill for skill in required_skills if skill.lower() not in [s.lower() for s in resume_skills]]
    missing_preferred = [skill for skill in preferred_skills if skill.lower() not in [s.lower() for s in resume_skills]]
    
    return {
        "overall_score": round(overall_score, 2),
        "skill_score": round(skill_score, 2),
        "experience_score": round(experience_score, 2),
        "skill_match_percentage": round(skill_match_percentage, 1),
        "experience_match_percentage": round(experience_match_percentage, 1),
        "recommendation_level": recommendation_level,
        "recommendation_text": recommendation_text,
        "color": color,
        "resume_years": resume_years,
        "required_years": required_years,
        "missing_required_skills": missing_required,
        "missing_preferred_skills": missing_preferred,
        "experience_level": experience_level,
        "industry": industry
    }

def extract_skills_with_gpt(text: str, context: str = "resume") -> List[str]:
    """
    Uses GPT to extract meaningful skills from text.
    context can be "resume" or "job_description"
    """
    prompt = f"""
You are a professional skills analyzer. Extract specific, relevant skills from the following {context} text.

IMPORTANT: Return ONLY a comma-separated list of skills, with no additional text, explanations, or formatting.

Focus on extracting:
1. Programming Languages: Python, Java, JavaScript, C++, C#, Ruby, PHP, Go, Rust, Swift, Kotlin, TypeScript, etc.
2. Frameworks & Libraries: React, Angular, Vue, Django, Flask, Spring, Node.js, Express, Laravel, ASP.NET, etc.
3. Tools & Technologies: Docker, Kubernetes, AWS, Azure, GCP, Git, Jenkins, Travis CI, etc.
4. Databases: MySQL, PostgreSQL, MongoDB, Redis, SQLite, Oracle, SQL Server, etc.
5. Frontend Technologies: HTML, CSS, SASS, LESS, Bootstrap, Tailwind, Material-UI, etc.
6. Data Science & ML: TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, Matplotlib, etc.
7. Soft Skills: Leadership, Communication, Problem Solving, Teamwork, Project Management, etc.
8. Industry Skills: Machine Learning, Data Analysis, Data Science, AI, Deep Learning, etc.
9. Methodologies: Agile, Scrum, Kanban, Waterfall, DevOps, CI/CD, etc.

Only include skills that are explicitly mentioned or clearly implied in the text. Do not infer skills that are not present.

Text to analyze:
{text}
"""
    
    try:
        response = call_gpt(prompt)
        # Clean up the response and split into individual skills
        skills = [skill.strip() for skill in response.split(',') if skill.strip()]
        # Remove any empty strings and duplicates
        skills = list(set([skill for skill in skills if skill and len(skill) > 1]))
        
        # If GPT returned very few skills, fall back to pattern matching
        if len(skills) < 3:
            print(f"[WARNING] GPT returned only {len(skills)} skills, falling back to pattern matching")
            pattern_skills = extract_basic_keywords(text)
            # Combine both methods, prioritizing GPT results
            combined_skills = list(set(skills + pattern_skills))
            return combined_skills
        
        return skills
    except Exception as e:
        print(f"[ERROR] Failed to extract skills with GPT: {str(e)}")
        print("[INFO] Falling back to pattern-based keyword extraction")
        # Fallback to basic keyword extraction
        return extract_basic_keywords(text)

def extract_basic_keywords(text: str) -> List[str]:
    """Fallback method for basic keyword extraction"""
    # Common technical skills patterns
    skill_patterns = [
        r'\b(?:Python|Java|JavaScript|C\+\+|C#|Ruby|PHP|Go|Rust|Swift|Kotlin|TypeScript|Scala|Perl|R|MATLAB)\b',
        r'\b(?:React|Angular|Vue|Django|Flask|Spring|Node\.js|Express|Laravel|ASP\.NET|FastAPI|Ruby on Rails)\b',
        r'\b(?:MySQL|PostgreSQL|MongoDB|Redis|SQLite|Oracle|SQL Server|Cassandra|DynamoDB|Neo4j)\b',
        r'\b(?:Docker|Kubernetes|AWS|Azure|GCP|Heroku|DigitalOcean|Vercel|Netlify|Firebase)\b',
        r'\b(?:Git|SVN|Jenkins|Travis CI|CircleCI|GitHub Actions|GitLab CI|Bitbucket Pipelines)\b',
        r'\b(?:HTML|CSS|SASS|LESS|Bootstrap|Tailwind|Material-UI|Ant Design|Chakra UI|Semantic UI)\b',
        r'\b(?:TensorFlow|PyTorch|Scikit-learn|Pandas|NumPy|Matplotlib|Seaborn|Plotly|Keras|OpenCV)\b',
        r'\b(?:Leadership|Communication|Problem Solving|Teamwork|Project Management|Collaboration)\b',
        r'\b(?:Machine Learning|Data Analysis|Data Science|AI|Deep Learning|Computer Vision|NLP)\b',
        r'\b(?:Agile|Scrum|Kanban|Waterfall|DevOps|CI/CD|TDD|BDD|Microservices|REST API)\b',
        r'\b(?:Linux|Unix|Windows|macOS|Shell|Bash|PowerShell|Ansible|Terraform|CloudFormation)\b',
        r'\b(?:Jira|Confluence|Slack|Teams|Zoom|Figma|Adobe Creative Suite|Photoshop|Illustrator)\b'
    ]
    
    skills = set()
    for pattern in skill_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        skills.update(matches)
    
    return list(skills)

def normalize_skills(skills: List[str]) -> List[str]:
    """Normalize skills for better matching (case-insensitive, remove duplicates)"""
    normalized = []
    seen = set()
    
    for skill in skills:
        # Normalize case and strip whitespace
        normalized_skill = skill.strip().lower()
        if normalized_skill and normalized_skill not in seen:
            normalized.append(skill.strip())  # Keep original case for display
            seen.add(normalized_skill)
    
    return normalized

def extract_keywords(text: str) -> List[str]:
    """Legacy function - now uses GPT-based extraction"""
    return extract_skills_with_gpt(text)

# --- OLD ANONYMIZATION (commented for fallback) ---
# def anonymize_text(text: str) -> Tuple[str, Dict[str, str]]:
#     """
#     Finds PII (persons, organizations) and replaces them with placeholders.
#     Returns the anonymized text and a map for de-anonymization.
#     """
#     anonymized_text = text
#     anonymization_map = {}
#     
#     # Look for full names (common pattern: FIRST LAST) - this is most important for resumes
#     # Use a more specific pattern to avoid false positives
#     full_name_pattern = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b'
#     full_names = re.findall(full_name_pattern, text)
#     
#     # Convert tuples to full names and filter out common false positives
#     full_names = [' '.join(name) for name in full_names]
#     # Filter out common job titles that might match the pattern
#     job_titles = ['software engineer', 'senior developer', 'junior developer', 'data scientist', 'project manager']
#     full_names = [name for name in full_names if name.lower() not in job_titles]
#     
#     # Also look for email addresses and phone numbers
#     email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
#     
#     emails = re.findall(email_pattern, text)
#     phones = re.findall(phone_pattern, text)
#     
#     # Use spaCy to find entities (but be more careful)
#     doc = nlp(text)
#     persons = []
#     orgs = []
#     
#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             # Only add if it's not part of a full name we already found
#             if not any(ent.text in full_name for full_name in full_names):
#                 # Also filter out job titles
#                 if ent.text.lower() not in job_titles:
#                     persons.append(ent.text)
#         elif ent.label_ == "ORG":
#             # Only add if it's not part of a full name we already found
#             if not any(ent.text in full_name for full_name in full_names):
#                 orgs.append(ent.text)
#     
#     persons = sorted(list(set(persons)))
#     orgs = sorted(list(set(orgs)))
#
#     # Replace full names first (these are most important for resume structure)
#     for i, full_name in enumerate(full_names):
#         placeholder = f"[PERSON_{i+1}]"
#         # Use regex for whole-word replacement to avoid replacing parts of words
#         anonymized_text = re.sub(r'\b' + re.escape(full_name) + r'\b', placeholder, anonymized_text)
#         anonymization_map[placeholder] = full_name
#
#     # Replace remaining persons (individual names not caught by full name pattern)
#     for i, person in enumerate(persons):
#         placeholder = f"[PERSON_{len(full_names) + i + 1}]"
#         anonymized_text = re.sub(r'\b' + re.escape(person) + r'\b', placeholder, anonymized_text)
#         anonymization_map[placeholder] = person
#
#     # Replace organizations
#     for i, org in enumerate(orgs):
#         placeholder = f"[ORG_{i+1}]"
#         anonymized_text = re.sub(r'\b' + re.escape(org) + r'\b', placeholder, anonymized_text)
#         anonymization_map[placeholder] = org
#     
#     # Replace emails
#     for i, email in enumerate(emails):
#         placeholder = f"[EMAIL_{i+1}]"
#         anonymized_text = anonymized_text.replace(email, placeholder)
#         anonymization_map[placeholder] = email
#     
#     # Replace phone numbers
#     for i, phone in enumerate(phones):
#         placeholder = f"[PHONE_{i+1}]"
#         anonymized_text = anonymized_text.replace(phone, placeholder)
#         anonymization_map[placeholder] = phone
#
#     return anonymized_text, anonymization_map

# --- NEW LLM-BASED EXTRACTION ---
def extract_resume_fields_with_llm(resume_text: str) -> dict:
    """
    Use GPT to extract all key resume fields as structured JSON from raw resume text.
    """
    prompt = f"""
You are an expert resume parser. Extract the following fields from the resume below and return ONLY a JSON object with this structure:
{{
  "name": string,
  "email": string,
  "phone": string,
  "location": string,
  "summary": string,
  "experience": [
    {{"company": string, "title": string, "start": string, "end": string, "bullets": [string]}}
  ],
  "education": [
    {{"degree": string, "institution": string, "year": string}}
  ],
  "skills": [string],
  "projects": [
    {{"name": string, "description": string}}
  ]
}}
IMPORTANT:
- The name should be the person's full name, not a job title or location.
- The email and phone should be valid if present.
- The summary should be 1-3 sentences summarizing the candidate.
- Experience and education should be arrays, even if only one entry.
- Skills should be a list of specific skills.
- Projects are optional.
- If a field is missing, use an empty string or empty array.

Resume:
{resume_text}
"""
    try:
        response = call_gpt(prompt)
        import json
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {}
    except Exception as e:
        print(f"[ERROR] Failed to extract resume fields with LLM: {str(e)}")
        return {}

# --- MAIN PIPELINE ---
def process_resume(resume_text: str, job_description: str, target_match_percentage: int = 0):
    """
    Uses LLM to extract structured resume fields and generates a LaTeX resume.
    """
    try:
        print(f"[DEBUG] Starting process_resume with resume length: {len(resume_text)}")
        # 1. Extract structured fields from resume using LLM
        resume_fields = extract_resume_fields_with_llm(resume_text)
        print(f"[DEBUG] Extracted fields: {resume_fields}")
        # 2. Extract skills for analysis (use LLM or fallback)
        resume_skills = resume_fields.get('skills', [])
        job_skills = extract_skills_with_gpt(job_description, "job_description")
        resume_skills = normalize_skills(resume_skills)
        job_skills = normalize_skills(job_skills)
        # 3. Calculate match score and recommendation
        match_analysis = calculate_match_score(resume_text, job_description, resume_skills, job_skills)
        # 4. Generate LaTeX resume using LLM
        prompt = f"""
You are a professional resume writer. Given the following structured resume data and job description, generate a complete, professional LaTeX resume. Use this structure:
- Name (large, bold at top)
- Contact info (email, phone, location)
- Summary
- Experience (with company, title, dates, bullet points)
- Education (degree, institution, year)
- Skills (as a list)
- Projects (if present)

STRUCTURED RESUME DATA:
{resume_fields}

JOB DESCRIPTION:
{job_description}

CRITICAL:
- The name must be the first and most prominent thing in the header.
- Do NOT use location or job title as the name.
- All sections must be present and properly formatted.
- Use only valid LaTeX.
- Make it look like a human professional resume.
- Do not hallucinate or invent information.
- If a field is missing, skip that section.
Return only the LaTeX code, ready to compile.
"""
        latex_content = call_gpt(prompt)
        print(f"[DEBUG] Generated LaTeX length: {len(latex_content)}")
        result = {
            "matched_skills": [s for s in resume_skills if s in job_skills],
            "missing_skills": [s for s in job_skills if s not in resume_skills],
            "latex_content": latex_content,
            "latex_filename": "tailored_resume.tex",
            "match_analysis": match_analysis
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
            "latex_filename": "error.tex",
            "match_analysis": {
                "overall_score": 0.0,
                "skill_score": 0.0,
                "experience_score": 0.0,
                "skill_match_percentage": 0.0,
                "experience_match_percentage": 0.0,
                "recommendation_level": "Error",
                "recommendation_text": "Unable to analyze due to processing error",
                "color": "red",
                "resume_years": 0,
                "required_years": 0,
                "missing_required_skills": [],
                "missing_preferred_skills": [],
                "experience_level": "unknown",
                "industry": "unknown"
            }
        }

#!/usr/bin/env python3
"""
Test script for skills extraction functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tailoring import extract_skills_with_gpt, normalize_skills

def test_skills_extraction():
    """Test the skills extraction functionality"""
    
    # Test resume text
    resume_text = """
    Software Engineer with 5 years of experience in Python development.
    Proficient in Django, Flask, and React. Experience with AWS, Docker, and Git.
    Strong background in machine learning using TensorFlow and scikit-learn.
    Led a team of 3 developers in an Agile environment.
    """
    
    # Test job description
    job_description = """
    We are looking for a Python Developer with experience in Django and React.
    Must have knowledge of AWS, Docker, and Git. Experience with machine learning
    frameworks like TensorFlow is a plus. Should be able to work in an Agile team.
    Knowledge of PostgreSQL and MongoDB is required.
    """
    
    print("Testing skills extraction...")
    print("=" * 50)
    
    # Extract skills from resume
    print("Extracting skills from resume...")
    resume_skills = extract_skills_with_gpt(resume_text, "resume")
    print(f"Resume skills: {resume_skills}")
    
    # Extract skills from job description
    print("\nExtracting skills from job description...")
    job_skills = extract_skills_with_gpt(job_description, "job_description")
    print(f"Job skills: {job_skills}")
    
    # Normalize skills
    print("\nNormalizing skills...")
    resume_skills_normalized = normalize_skills(resume_skills)
    job_skills_normalized = normalize_skills(job_skills)
    
    print(f"Normalized resume skills: {resume_skills_normalized}")
    print(f"Normalized job skills: {job_skills_normalized}")
    
    # Find matches
    resume_set = set(skill.lower() for skill in resume_skills_normalized)
    job_set = set(skill.lower() for skill in job_skills_normalized)
    
    matched_skills = resume_set & job_set
    missing_skills = job_set - resume_set
    
    print(f"\nMatched skills: {list(matched_skills)}")
    print(f"Missing skills: {list(missing_skills)}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_skills_extraction()

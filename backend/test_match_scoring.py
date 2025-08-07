#!/usr/bin/env python3
"""
Test script for match scoring and recommendation functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tailoring import (
    extract_skills_with_gpt, 
    normalize_skills, 
    calculate_match_score,
    extract_experience_years,
    extract_job_requirements
)

def test_match_scoring():
    """Test the comprehensive match scoring functionality"""
    
    # Test resume text with experience
    resume_text = """
    SENIOR SOFTWARE ENGINEER
    
    EXPERIENCE:
    Senior Software Engineer at TechCorp (2020-2023) - 3 years
    - Led development of Python-based web applications using Django and React
    - Managed AWS infrastructure and Docker containerization
    - Implemented CI/CD pipelines with Jenkins and Git
    
    Software Engineer at StartupXYZ (2018-2020) - 2 years
    - Developed REST APIs using Flask and PostgreSQL
    - Worked with machine learning models using TensorFlow
    - Collaborated in Agile development environment
    
    EDUCATION:
    Bachelor's in Computer Science
    
    SKILLS:
    Python, Django, Flask, React, AWS, Docker, Git, Jenkins, PostgreSQL, TensorFlow, Machine Learning, Agile
    """
    
    # Test job description with requirements
    job_description = """
    SENIOR PYTHON DEVELOPER
    
    We are seeking a Senior Python Developer with 5+ years of experience to join our team.
    
    REQUIREMENTS:
    - 5+ years of professional software development experience
    - Strong proficiency in Python, Django, and React
    - Experience with AWS cloud services and Docker
    - Knowledge of PostgreSQL and Git
    - Experience with CI/CD pipelines
    - Bachelor's degree in Computer Science or related field
    
    PREFERRED SKILLS:
    - Experience with machine learning frameworks (TensorFlow, PyTorch)
    - Knowledge of Kubernetes and microservices
    - Experience with Agile/Scrum methodologies
    - Background in data science or analytics
    
    RESPONSIBILITIES:
    - Develop and maintain web applications
    - Collaborate with cross-functional teams
    - Mentor junior developers
    - Participate in code reviews and technical discussions
    """
    
    print("Testing Comprehensive Match Scoring...")
    print("=" * 60)
    
    # Extract skills
    print("1. Extracting skills...")
    resume_skills = extract_skills_with_gpt(resume_text, "resume")
    job_skills = extract_skills_with_gpt(job_description, "job_description")
    
    resume_skills = normalize_skills(resume_skills)
    job_skills = normalize_skills(job_skills)
    
    print(f"Resume skills: {resume_skills}")
    print(f"Job skills: {job_skills}")
    
    # Extract experience years
    print("\n2. Extracting experience...")
    resume_years = extract_experience_years(resume_text)
    print(f"Resume years of experience: {resume_years}")
    
    # Extract job requirements
    print("\n3. Extracting job requirements...")
    job_requirements = extract_job_requirements(job_description)
    print(f"Job requirements: {job_requirements}")
    
    # Calculate match score
    print("\n4. Calculating match score...")
    match_analysis = calculate_match_score(resume_text, job_description, resume_skills, job_skills)
    
    # Display results
    print("\n" + "=" * 60)
    print("MATCH ANALYSIS RESULTS")
    print("=" * 60)
    
    print(f"Overall Match Score: {match_analysis['overall_score']:.2f}")
    print(f"Recommendation: {match_analysis['recommendation_level']}")
    print(f"Color Code: {match_analysis['color']}")
    print(f"Recommendation Text: {match_analysis['recommendation_text']}")
    
    print(f"\nDetailed Breakdown:")
    print(f"- Skill Match Score: {match_analysis['skill_score']:.2f} ({match_analysis['skill_match_percentage']:.1f}%)")
    print(f"- Experience Match Score: {match_analysis['experience_score']:.2f} ({match_analysis['experience_match_percentage']:.1f}%)")
    
    print(f"\nExperience Analysis:")
    print(f"- Your Experience: {match_analysis['resume_years']} years")
    print(f"- Required Experience: {match_analysis['required_years']} years")
    print(f"- Experience Level: {match_analysis['experience_level']}")
    print(f"- Industry: {match_analysis['industry']}")
    
    print(f"\nSkill Gaps:")
    if match_analysis['missing_required_skills']:
        print(f"- Missing Required Skills: {', '.join(match_analysis['missing_required_skills'])}")
    else:
        print("- Missing Required Skills: None")
        
    if match_analysis['missing_preferred_skills']:
        print(f"- Missing Preferred Skills: {', '.join(match_analysis['missing_preferred_skills'])}")
    else:
        print("- Missing Preferred Skills: None")
    
    print("\n" + "=" * 60)
    print("Test completed!")

def test_different_scenarios():
    """Test different match scenarios"""
    
    scenarios = [
        {
            "name": "Perfect Match",
            "resume": "Senior Developer with 8 years experience in Python, Django, React, AWS, Docker, PostgreSQL, Git, Jenkins, TensorFlow, Machine Learning, Agile",
            "job": "Senior Python Developer with 5+ years experience. Required: Python, Django, React, AWS, Docker, PostgreSQL, Git. Preferred: TensorFlow, Machine Learning, Agile"
        },
        {
            "name": "Good Match",
            "resume": "Developer with 4 years experience in Python, Django, React, AWS, Git",
            "job": "Python Developer with 3+ years experience. Required: Python, Django, React, AWS. Preferred: Docker, PostgreSQL, Machine Learning"
        },
        {
            "name": "Weak Match",
            "resume": "Junior Developer with 1 year experience in JavaScript, HTML, CSS",
            "job": "Senior Python Developer with 5+ years experience. Required: Python, Django, React, AWS, Docker"
        }
    ]
    
    print("\n" + "=" * 60)
    print("TESTING DIFFERENT SCENARIOS")
    print("=" * 60)
    
    for scenario in scenarios:
        print(f"\nScenario: {scenario['name']}")
        print("-" * 40)
        
        resume_skills = extract_skills_with_gpt(scenario['resume'], "resume")
        job_skills = extract_skills_with_gpt(scenario['job'], "job_description")
        
        resume_skills = normalize_skills(resume_skills)
        job_skills = normalize_skills(job_skills)
        
        match_analysis = calculate_match_score(scenario['resume'], scenario['job'], resume_skills, job_skills)
        
        print(f"Score: {match_analysis['overall_score']:.2f}")
        print(f"Recommendation: {match_analysis['recommendation_level']}")
        print(f"Skills: {match_analysis['skill_match_percentage']:.1f}%")
        print(f"Experience: {match_analysis['experience_match_percentage']:.1f}%")

if __name__ == "__main__":
    test_match_scoring()
    test_different_scenarios()

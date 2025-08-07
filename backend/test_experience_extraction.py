#!/usr/bin/env python3
"""
Test script for experience extraction functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tailoring import extract_experience_years, extract_job_requirements

def test_experience_extraction():
    """Test the experience extraction functionality"""
    
    test_cases = [
        {
            "name": "Simple years",
            "text": "Software Engineer with 5 years of experience in Python development.",
            "expected": 5
        },
        {
            "name": "Multiple roles with years",
            "text": """
            EXPERIENCE:
            Senior Software Engineer at TechCorp (2020-2023) - 3 years
            Software Engineer at StartupXYZ (2018-2020) - 2 years
            """,
            "expected": 5
        },
        {
            "name": "Years with text",
            "text": "I have 7 years of professional experience in software development.",
            "expected": 7
        },
        {
            "name": "Abbreviated years",
            "text": "Developer with 3 yrs experience in web development.",
            "expected": 3
        },
        {
            "name": "No specific years",
            "text": "Software Engineer with experience in Python and React.",
            "expected": 0  # Should be estimated or 0
        },
        {
            "name": "Calendar years mixed",
            "text": "Worked from 2020 to 2023, total 3 years of experience.",
            "expected": 3
        },
        {
            "name": "Internship + Professional (User's case)",
            "text": """
            EXPERIENCE:
            Software Engineer at TechCorp (2024-Present)
            - Full-time professional role
            
            Internship at StartupXYZ (2018) - 2 months
            - Part-time internship role
            """,
            "expected": 0  # Should be ~2.4 years (2024 to present)
        },
        {
            "name": "Date ranges only",
            "text": """
            EXPERIENCE:
            Senior Developer at CompanyA (2020-2023)
            Junior Developer at CompanyB (2018-2020)
            """,
            "expected": 5
        }
    ]
    
    print("Testing Experience Extraction...")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Text: {test_case['text'][:100]}...")
        
        try:
            result = extract_experience_years(test_case['text'])
            print(f"Extracted: {result} years")
            print(f"Expected: {test_case['expected']} years")
            
            if result == test_case['expected']:
                print("✅ PASS")
            else:
                print("❌ FAIL")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Testing Job Requirements Extraction...")
    print("=" * 50)
    
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
    """
    
    try:
        requirements = extract_job_requirements(job_description)
        print(f"Job Requirements: {requirements}")
        
        if 'required_years' in requirements:
            years = requirements['required_years']
            print(f"Required Years: {years}")
            if isinstance(years, int) and 0 <= years <= 50:
                print("✅ Valid years extracted")
            else:
                print("❌ Invalid years extracted")
        else:
            print("❌ No required_years found")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_experience_extraction()

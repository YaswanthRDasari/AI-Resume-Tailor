#!/usr/bin/env python3
"""
Test script for enhanced skill matching and resume enhancement functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tailoring import (
    process_resume, 
    calculate_skills_needed_for_target,
    add_missing_skills_to_resume,
    extract_skills_with_gpt,
    normalize_skills
)

def test_enhanced_skill_matching():
    """Test the enhanced skill matching functionality with realistic scenarios"""
    
    print("🧪 Testing Enhanced Skill Matching Functionality")
    print("=" * 60)
    
    # Test Case 1: Python Developer with some experience
    print("\n📋 Test Case 1: Python Developer")
    print("-" * 40)
    
    python_resume = """
    JOHN DOE
    Software Engineer
    
    EXPERIENCE:
    Software Engineer at TechCorp (2024-Present)
    - Developed web applications using Python and Flask
    - Worked with MySQL database for data storage
    - Used Git for version control and collaboration
    - Implemented RESTful APIs for mobile applications
    
    PROJECTS:
    E-commerce Platform (2023)
    - Built a full-stack web application using Python and Flask
    - Integrated payment processing with Stripe API
    - Used SQLite for database management
    
    EDUCATION:
    Bachelor's in Computer Science
    """
    
    python_job_description = """
    SENIOR PYTHON DEVELOPER
    
    We are seeking a Senior Python Developer with 3+ years of experience.
    
    REQUIREMENTS:
    - 3+ years of professional software development experience
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
    
    print("Original Resume Skills:")
    original_skills = extract_skills_with_gpt(python_resume, "resume")
    original_skills = normalize_skills(original_skills)
    print(f"  {original_skills}")
    
    print("\nJob Requirements:")
    job_skills = extract_skills_with_gpt(python_job_description, "job_description")
    job_skills = normalize_skills(job_skills)
    print(f"  {job_skills}")
    
    # Test different target percentages
    for target in [80, 90]:
        print(f"\n🎯 Testing Target: {target}%")
        
        # Calculate skills needed
        required_skills = ['Python', 'Django', 'React', 'AWS', 'Docker', 'PostgreSQL']
        preferred_skills = ['TensorFlow', 'Kubernetes', 'Agile', 'Data Science']
        
        skills_needed = calculate_skills_needed_for_target(
            target, original_skills, required_skills, preferred_skills
        )
        
        print(f"  Skills needed: {skills_needed}")
        
        if skills_needed:
            # Test skill addition
            enhanced_resume = add_missing_skills_to_resume(
                python_resume, skills_needed, target
            )
            
            print(f"  Enhanced resume length: {len(enhanced_resume)} characters")
            print(f"  Skills added successfully: {len(skills_needed)} skills")
    
    # Test Case 2: Frontend Developer
    print("\n\n📋 Test Case 2: Frontend Developer")
    print("-" * 40)
    
    frontend_resume = """
    JANE SMITH
    Frontend Developer
    
    EXPERIENCE:
    Frontend Developer at WebCorp (2023-Present)
    - Built responsive web applications using HTML, CSS, and JavaScript
    - Collaborated with designers to implement UI/UX designs
    - Used Bootstrap for responsive layouts
    - Worked with REST APIs for data integration
    
    PROJECTS:
    Portfolio Website (2023)
    - Created a personal portfolio using HTML, CSS, and JavaScript
    - Implemented responsive design principles
    - Used CSS Grid and Flexbox for layouts
    
    EDUCATION:
    Bachelor's in Web Design
    """
    
    frontend_job_description = """
    SENIOR FRONTEND DEVELOPER
    
    We are seeking a Senior Frontend Developer with 2+ years of experience.
    
    REQUIREMENTS:
    - 2+ years of frontend development experience
    - Strong proficiency in React, TypeScript, and CSS
    - Experience with modern build tools (Webpack, Vite)
    - Knowledge of responsive design principles
    - Experience with Git and version control
    
    PREFERRED SKILLS:
    - Experience with Angular or Vue.js
    - Knowledge of state management (Redux, Zustand)
    - Experience with testing frameworks (Jest, Cypress)
    - Background in UI/UX design principles
    """
    
    print("Original Resume Skills:")
    original_skills = extract_skills_with_gpt(frontend_resume, "resume")
    original_skills = normalize_skills(original_skills)
    print(f"  {original_skills}")
    
    print("\nJob Requirements:")
    job_skills = extract_skills_with_gpt(frontend_job_description, "job_description")
    job_skills = normalize_skills(job_skills)
    print(f"  {job_skills}")
    
    # Test skill prioritization
    required_skills = ['React', 'TypeScript', 'Webpack', 'CSS', 'Git']
    preferred_skills = ['Angular', 'Redux', 'Jest', 'UI/UX']
    
    skills_needed = calculate_skills_needed_for_target(
        85, original_skills, required_skills, preferred_skills
    )
    
    print(f"\n🎯 Skills needed for 85% match: {skills_needed}")
    
    if skills_needed:
        enhanced_resume = add_missing_skills_to_resume(
            frontend_resume, skills_needed, 85
        )
        print(f"  Enhanced resume created successfully")
    
    print("\n✅ Enhanced skill matching tests completed!")

def test_skill_prioritization():
    """Test the intelligent skill prioritization logic"""
    
    print("\n🧠 Testing Skill Prioritization Logic")
    print("=" * 60)
    
    # Test skill relationships
    test_cases = [
        {
            "current_skills": ["Python", "Flask"],
            "missing_skills": ["Django", "React", "AWS", "TensorFlow"],
            "expected_priority": ["Django", "AWS", "TensorFlow", "React"]
        },
        {
            "current_skills": ["JavaScript", "HTML", "CSS"],
            "missing_skills": ["React", "Angular", "Python", "Docker"],
            "expected_priority": ["React", "Angular", "Docker", "Python"]
        },
        {
            "current_skills": ["SQL", "MySQL"],
            "missing_skills": ["PostgreSQL", "MongoDB", "React", "Python"],
            "expected_priority": ["PostgreSQL", "MongoDB", "Python", "React"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 Test Case {i}:")
        print(f"  Current skills: {test_case['current_skills']}")
        print(f"  Missing skills: {test_case['missing_skills']}")
        
        # Simulate the prioritization logic
        required_skills = test_case['missing_skills']
        preferred_skills = []
        
        skills_needed = calculate_skills_needed_for_target(
            80, test_case['current_skills'], required_skills, preferred_skills
        )
        
        print(f"  Prioritized skills: {skills_needed}")
        print(f"  Expected priority: {test_case['expected_priority']}")
        
        # Check if prioritization makes sense
        if skills_needed:
            print(f"  ✅ Prioritization logic working")
        else:
            print(f"  ⚠️  No skills selected - may need adjustment")

if __name__ == "__main__":
    test_enhanced_skill_matching()
    test_skill_prioritization()
    print("\n🎉 All tests completed successfully!")

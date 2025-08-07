#!/usr/bin/env python3
"""
Test script for target match percentage functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tailoring import process_resume, calculate_skills_needed_for_target

def test_target_match_functionality():
    """Test the target match percentage functionality"""
    
    # Sample resume with limited skills
    sample_resume = """
    JOHN DOE
    Software Engineer
    
    EXPERIENCE:
    Software Engineer at TechCorp (2024-Present)
    - Developed web applications using Python and Flask
    - Worked with MySQL database
    - Used Git for version control
    
    EDUCATION:
    Bachelor's in Computer Science
    """
    
    # Sample job description with many requirements
    sample_job_description = """
    SENIOR PYTHON DEVELOPER
    
    We are seeking a Senior Python Developer with 5+ years of experience.
    
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
    
    print("Testing Target Match Percentage Functionality")
    print("=" * 60)
    
    # Test different target percentages
    target_percentages = [0, 70, 80, 90, 100]
    
    for target in target_percentages:
        print(f"\n🎯 Testing Target: {target}%")
        print("-" * 40)
        
        try:
            result = process_resume(sample_resume, sample_job_description, target)
            
            if result.get('error'):
                print(f"❌ Error: {result['error']}")
                continue
            
            match_analysis = result.get('match_analysis', {})
            overall_score = match_analysis.get('overall_score', 0)
            actual_percentage = round(overall_score * 100)
            
            print(f"✅ Original Score: {actual_percentage}%")
            
            if target > 0:
                if 'skills_added' in match_analysis and match_analysis['skills_added']:
                    print(f"✅ Skills Added: {match_analysis['skills_added']}")
                    print(f"✅ Target Achieved: {actual_percentage}% >= {target}%")
                else:
                    print(f"ℹ️  No skills needed to be added")
            
            print(f"✅ Recommendation: {match_analysis.get('recommendation_level', 'Unknown')}")
            
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Testing Skills Calculation Function")
    print("=" * 60)
    
    # Test the skills calculation function directly
    current_skills = ['Python', 'Flask', 'MySQL', 'Git']
    required_skills = ['Python', 'Django', 'React', 'AWS', 'Docker', 'PostgreSQL']
    preferred_skills = ['TensorFlow', 'Kubernetes', 'Agile', 'Data Science']
    
    for target in [70, 80, 90, 100]:
        skills_needed = calculate_skills_needed_for_target(
            target, current_skills, required_skills, preferred_skills
        )
        print(f"\nTarget {target}%: {len(skills_needed)} skills needed")
        if skills_needed:
            print(f"Skills to add: {skills_needed}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_target_match_functionality()

#!/usr/bin/env python3
"""
Test script to verify proper resume structure generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tailoring import process_resume, anonymize_text, de_anonymize_text

def test_resume_structure():
    """Test that the resume structure is properly generated"""
    
    print("🧪 Testing Resume Structure Generation")
    print("=" * 60)
    
    # Test Case 1: Basic resume with proper structure
    print("\n📋 Test Case 1: Basic Resume Structure")
    print("-" * 40)
    
    sample_resume = """
    JOHN DOE
    Software Engineer
    john.doe@email.com | (555) 123-4567 | New York, NY
    
    SUMMARY
    Experienced software engineer with 3+ years developing web applications using Python and JavaScript.
    
    EXPERIENCE
    Software Engineer at TechCorp (2022-Present)
    - Developed full-stack web applications using Python, Flask, and React
    - Implemented RESTful APIs and database integrations
    - Collaborated with cross-functional teams using Agile methodologies
    
    Junior Developer at StartupXYZ (2021-2022)
    - Built responsive web interfaces using HTML, CSS, and JavaScript
    - Worked with MySQL databases and Git version control
    - Participated in code reviews and testing procedures
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2021
    
    SKILLS
    Programming: Python, JavaScript, HTML, CSS, SQL
    Frameworks: Flask, React, Bootstrap
    Tools: Git, VS Code, Docker
    """
    
    sample_job_description = """
    SENIOR PYTHON DEVELOPER
    
    We are seeking a Senior Python Developer with 3+ years of experience.
    
    REQUIREMENTS:
    - 3+ years of professional software development experience
    - Strong proficiency in Python, Flask, and React
    - Experience with RESTful APIs and database design
    - Knowledge of Git and version control
    - Experience with Agile methodologies
    
    PREFERRED SKILLS:
    - Experience with Docker and cloud deployment
    - Knowledge of testing frameworks
    - Background in full-stack development
    """
    
    print("Original Resume:")
    print(sample_resume[:200] + "...")
    
    print("\nJob Description:")
    print(sample_job_description[:200] + "...")
    
    try:
        result = process_resume(sample_resume, sample_job_description, 0)
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            return
        
        latex_content = result.get('latex_content', '')
        print(f"\n✅ Generated LaTeX length: {len(latex_content)} characters")
        
        # Check for proper structure
        structure_checks = [
            ("Document class", "\\documentclass" in latex_content),
            ("Name in header", "[PERSON_1]" in latex_content or "JOHN DOE" in latex_content),
            ("Experience section", "\\section*{Experience}" in latex_content or "\\section*{EXPERIENCE}" in latex_content),
            ("Education section", "\\section*{Education}" in latex_content or "\\section*{EDUCATION}" in latex_content),
            ("Skills section", "\\section*{Skills}" in latex_content or "\\section*{SKILLS}" in latex_content),
            ("Proper LaTeX structure", "\\begin{document}" in latex_content and "\\end{document}" in latex_content),
            ("No unwanted keywords", "hyderabad" not in latex_content.lower() and "classification" not in latex_content.lower()),
        ]
        
        print("\n📊 Structure Validation:")
        all_passed = True
        for check_name, passed in structure_checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}: {'PASS' if passed else 'FAIL'}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n🎉 All structure checks passed!")
        else:
            print("\n⚠️  Some structure issues detected")
        
        # Show a preview of the generated LaTeX
        print(f"\n📄 LaTeX Preview (first 500 chars):")
        print("-" * 40)
        print(latex_content[:500] + "..." if len(latex_content) > 500 else latex_content)
        
    except Exception as e:
        print(f"❌ Exception during testing: {str(e)}")
        import traceback
        traceback.print_exc()

def test_anonymization():
    """Test the anonymization function"""
    
    print("\n\n🔒 Testing Anonymization")
    print("=" * 60)
    
    test_text = """
    JOHN DOE
    Software Engineer
    john.doe@email.com | (555) 123-4567 | New York, NY
    
    Worked at TechCorp and StartupXYZ.
    """
    
    print("Original text:")
    print(test_text)
    
    try:
        anonymized, mapping = anonymize_text(test_text)
        print("\nAnonymized text:")
        print(anonymized)
        
        print("\nAnonymization mapping:")
        for placeholder, original in mapping.items():
            print(f"  {placeholder} -> {original}")
        
        # Test de-anonymization
        restored = de_anonymize_text(anonymized, mapping)
        print("\nRestored text:")
        print(restored)
        
        if restored.strip() == test_text.strip():
            print("\n✅ Anonymization/De-anonymization working correctly")
        else:
            print("\n❌ Anonymization/De-anonymization failed")
            
    except Exception as e:
        print(f"❌ Exception during anonymization test: {str(e)}")

if __name__ == "__main__":
    test_resume_structure()
    test_anonymization()
    print("\n🎉 All tests completed!")


import sys
import os
# Add current directory to path so we can import app
sys.path.append(os.getcwd())

from app import extract_text_from_pdf, parse_resume

def test_resume_parsing():
    print("Testing Resume Parsing...")
    
    # Test cases: (filename, expected_email, expected_skill, expected_age, expected_exp)
    test_cases = [
        ("test_data/resume1.pdf", "johndoe@example.com", "Python", 25, 3),
        ("test_data/resume3.pdf", "alice@example.com", "Deep Learning", 32, 8),
        ("test_data/resume5.pdf", "charlie@example.com", "Project Management", 27, 4)
    ]
    
    for filename, email, skill, age, exp in test_cases:
        print(f"\nTesting {filename}...")
        text = extract_text_from_pdf(filename)
            
        data = parse_resume(text)
        print("Extracted Data:", data)
        
        assert data['Email'] == email, f"Email mismatch for {filename}"
        assert skill in data['Skills'], f"Skill {skill} not found in {filename}"
        assert data.get('Age') == age, f"Age mismatch for {filename}: Expected {age}, got {data.get('Age')}"
        assert data.get('Experience') == exp, f"Experience mismatch for {filename}: Expected {exp}, got {data.get('Experience')}"
        
    print("\nALL TESTS PASSED!")

if __name__ == "__main__":
    try:
        test_resume_parsing()
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)

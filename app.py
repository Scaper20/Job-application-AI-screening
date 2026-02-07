
import streamlit as st
import joblib
import pandas as pd
import numpy as np
import pdfplumber
import re
import os

model = joblib.load("model/logistic_model.pkl")
scaler = joblib.load("model/scaler.pkl")

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text



def parse_resume(text):
    data = {}
    
    # Simple regex patterns
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    
    email_match = re.search(email_pattern, text)
    phone_match = re.search(phone_pattern, text)
    
    data['Email'] = email_match.group(0) if email_match else "Not Found"
    data['Phone'] = phone_match.group(0) if phone_match else "Not Found"
    
    # Skills extraction (keyword based)
    skills_list = ['Python', 'Java', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau', 'Networking']
    extracted_skills = [skill for skill in skills_list if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]
    data['Skills'] = extracted_skills

    # Age extraction
    age_match = re.search(r'Age:\s*(\d+)', text, re.IGNORECASE)
    if age_match:
        data['Age'] = int(age_match.group(1))

    # Experience extraction
    exp_match = re.search(r'Experience:\s*(\d+)', text, re.IGNORECASE)
    if exp_match:
        data['Experience'] = int(exp_match.group(1))
    
    # Heuristics for other fields
    # Education Level
    if re.search(r'PhD|Doctorate', text, re.IGNORECASE):
        data['Education'] = "PhD"
    elif re.search(r'Master|M\.Sc|MBA', text, re.IGNORECASE):
        data['Education'] = "Masters"
    elif re.search(r'Bachelor|B\.Sc|B\.E|B\.Tech', text, re.IGNORECASE):
        data['Education'] = "Bachelors"
    elif re.search(r'Diploma', text, re.IGNORECASE):
        data['Education'] = "Diploma"
    else:
        data['Education'] = "Bachelors" # Default
        
    return data

def main():
    st.title("Human–AI Job Applicant Screening System")

    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

    extracted_data = {}
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            
            extracted_data = parse_resume(resume_text)
            st.success("Resume Parsed Successfully!")
            st.write(f"**Extracted Email:** {extracted_data.get('Email')}")
            st.write(f"**Extracted Skills:** {', '.join(extracted_data.get('Skills', []))}")
            st.write(f"**Extracted Age:** {extracted_data.get('Age', 'Not Found')}")
            st.write(f"**Extracted Experience:** {extracted_data.get('Experience', 'Not Found')} years")
            
        except Exception as e:
            st.error(f"Error parsing file: {e}")

    st.subheader("Enter Applicant Details")

    # Auto-fill logic
    default_edu_index = 1 # Bachelors
    if 'Education' in extracted_data:
        options = ["Diploma", "Bachelors", "Masters"]
        if extracted_data['Education'] in options:
            default_edu_index = options.index(extracted_data['Education'])

    # Skill score estimation (very basic based on count of skills)
    default_skill_score = 70
    if 'Skills' in extracted_data:
        default_skill_score = min(100, 50 + len(extracted_data['Skills']) * 10)

    # Defaults for Age and Experience
    default_age = extracted_data.get('Age', 25)
    default_experience = extracted_data.get('Experience', 2)

    age = st.number_input("Age", 18, 60, default_age)
    education = st.selectbox("Education Level", ["Diploma", "Bachelors", "Masters"], index=default_edu_index)
    experience = st.number_input("Years of Experience", 0, 40, default_experience)
    skill = st.slider("Skill Score", 0, 100, default_skill_score)
    interview = st.slider("Interview Score", 0, 100, 65)
    company = st.slider("Previous Company Rating", 1, 5, 3)

    if st.button("Predict"):
        # CREATE ALL REQUIRED MODEL FEATURES
        input_dict = {
            "Age": age,
            "Years_Experience": experience,
            "Skill_Score": skill,
            "Interview_Score": interview,
            "Company_Rating": company,

            "Education_Level_Diploma": 0,
            "Education_Level_Masters": 0,
        }

        # SET THE CORRECT DUMMY VALUE
        if education == "Diploma":
            input_dict["Education_Level_Diploma"] = 1
        elif education == "Masters":
            input_dict["Education_Level_Masters"] = 1
        # If user selects Bachelors → both remain 0, automatically correct

        # CONVERT TO DATAFRAME
        input_df = pd.DataFrame([input_dict])

        # SCALE
        input_scaled = scaler.transform(input_df)

        # PREDICT
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]

        st.subheader("AI Recommendation")
        st.write("✓ Selected" if prediction == 1 else "✗ Not Selected")
        st.write(f"Confidence Score: {probability:.2f}")

if __name__ == "__main__":
    main()

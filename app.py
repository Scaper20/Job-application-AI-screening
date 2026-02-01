import streamlit as st
import joblib
import pandas as pd
import numpy as np

model = joblib.load("model/logistic_model.pkl")
scaler = joblib.load("model/scaler.pkl")

st.title("Human–AI Job Applicant Screening System")

st.subheader("Enter Applicant Details")

age = st.number_input("Age", 18, 60, 25)
education = st.selectbox("Education Level", ["Diploma", "Bachelors", "Masters"])
experience = st.number_input("Years of Experience", 0, 40, 2)
skill = st.slider("Skill Score", 0, 100, 70)
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

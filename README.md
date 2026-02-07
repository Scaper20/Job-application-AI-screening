# Human–AI Job Applicant Screening System

An AI-powered application to streamline the hiring process. This system predicts whether a candidate should be selected based on their details and supports automated resume parsing.

## 🚀 Features

- **AI Prediction Application**:
  - Predicts candidate selection probability using a Logistic Regression model.
  - Visual output: "Selected" or "Not Selected" with a confidence score.
- **Resume Parsing**:
  - 📄 Upload PDF resumes.
  - 🤖 Automatically extracts:
    - **Contact Info** (Email, Phone)
    - **Age**
    - **Years of Experience**
    - **Skills** (Matches against a predefined tech stack)
    - **Education Level** (Diploma, Bachelors, Masters, PhD)
  - Auto-fills the screening form fields based on extracted data.
- **Explainability**:
  - Uses SHAP (SHapley Additive exPlanations) to interpret model decisions (see `outputs/shap_summary.png`).

## 🛠️ Installation & Setup

1.  **Clone the repository** (if applicable) or navigate to the project folder.
2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Usage

### 1. Run the Application
Start the Streamlit web interface:
```bash
streamlit run app.py
```

### 2. Using the App
- **Manual Entry**: Enter Age, Education, Experience, etc., and click "Predict".
- **Resume Upload**:
    1. Expand the "Upload Resume" section.
    2. Drag and drop a `.pdf` file.
    3. Watch as the form fields (Education, Skills Score) are automatically populated!

### 3. Retrain the Model (Optional)
If you want to regenerate the model or data:
```bash
# Generate dummy data
python generate_data.py

# Train the model and save artifacts
python train.py
```

## 📂 Project Structure

- `app.py`: Main Streamlit application file.
- `train.py`: Script to train the Logistic Regression model.
- `generate_data.py`: Script to generate synthetic training data.
- `requirements.txt`: Python dependencies.
- `model/`: Directory containing saved model artifacts (`logistic_model.pkl`, `scaler.pkl`).
- `data/`: Contains the dataset `job_applicants.csv`.
- `outputs/`: Stores performance plots and SHAP summaries.

## 🧪 Testing

To verify the resume parsing logic:
```bash
# Generates sample PDF files and runs tests
python generate_test_resumes.py
python test_parsing.py
```

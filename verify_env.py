
try:
    import streamlit
    print("streamlit imported successfully")
    import joblib
    print("joblib imported successfully")
    import pandas
    print("pandas imported successfully")
    import numpy
    print("numpy imported successfully")
    import pdfplumber
    print("pdfplumber imported successfully")
    import docx
    print("python-docx imported successfully")
    import re
    print("re imported successfully")
    print("\nALL IMPORTS SUCCESSFUL! The environment is ready.")
except ImportError as e:
    print(f"\nIMPORT ERROR: {e}")
    exit(1)
except Exception as e:
    print(f"\nERROR: {e}")
    exit(1)

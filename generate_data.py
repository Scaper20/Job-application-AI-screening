import pandas as pd
import numpy as np

np.random.seed(42)

rows = 100

data = {
    "Age": np.random.randint(22, 45, rows),
    "Education_Level": np.random.choice(
        ["Diploma", "Bachelors", "Masters"], rows, p=[0.3, 0.45, 0.25]
    ),
    "Years_Experience": np.random.randint(0, 20, rows),
    "Skill_Score": np.random.randint(50, 100, rows),
    "Interview_Score": np.random.randint(50, 100, rows),
    "Company_Rating": np.random.randint(1, 6, rows),
}

df = pd.DataFrame(data)

# Simple logic for selection (makes data realistic)
df["Selected"] = (
    (df["Skill_Score"] > 70) &
    (df["Interview_Score"] > 65) &
    (df["Years_Experience"] > 2)
).astype(int)

df.to_csv("data/job_applicants.csv", index=False)

print("Dataset created with", len(df), "rows")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("data/job_applicants.csv")

# Drop missing values
df = df.dropna()

# Separate features and target
X = df.drop("Selected", axis=1)
y = df["Selected"]

# Encode categorical variables
X = pd.get_dummies(X, drop_first=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(X.columns.tolist())


# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("Training set size:", X_train.shape)
print("Test set size:", X_test.shape)


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("\nACCURACY:", accuracy_score(y_test, y_pred))
print("\nCLASSIFICATION REPORT:\n", classification_report(y_test, y_pred))
print("\nCONFUSION MATRIX:\n", confusion_matrix(y_test, y_pred))



import joblib
import os

os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/logistic_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")



import shap

# Use a small sample for SHAP
explainer = shap.Explainer(model, X_train)
shap_values = explainer(X_test[:10])

# Save a SHAP summary plot
shap.summary_plot(shap_values, show=False)

import matplotlib.pyplot as plt
plt.savefig("outputs/shap_summary.png", bbox_inches="tight")


feature_importance = pd.Series(
    model.coef_[0], index=X.columns
).sort_values(ascending=False)

print("\nFEATURE IMPORTANCE:")
print(feature_importance)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, model.predict(X_test))
disp = ConfusionMatrixDisplay(cm)
disp.plot()
plt.savefig("outputs/confusion_matrix.png", bbox_inches="tight")
plt.close()


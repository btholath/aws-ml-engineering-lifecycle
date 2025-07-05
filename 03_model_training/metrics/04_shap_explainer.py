"""
SHAP explanation of XGBoost model.
"""
import shap, xgboost, pandas as pd, joblib, matplotlib.pyplot as plt

model = joblib.load("model.joblib")
df = pd.read_csv("test_data.csv")
X_test = df.drop(columns=["label"])

explainer = shap.Explainer(model)
shap_values = explainer(X_test)

shap.summary_plot(shap_values, X_test, show=False)
plt.savefig("shap_summary.png")

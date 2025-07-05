import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd, joblib

df = pd.read_csv("test_data.csv")
X_test, y_test = df.drop(columns=["label"]), df["label"]
model = joblib.load("model.joblib")
y_scores = model.predict_proba(X_test)[:, 1]

fpr, tpr, _ = roc_curve(y_test, y_scores)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig("roc_curve.png")

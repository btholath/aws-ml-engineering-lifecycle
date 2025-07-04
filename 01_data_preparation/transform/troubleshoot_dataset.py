import pandas as pd

df = pd.read_csv('./dataset/sample_loan_ready_for_xgboost.csv', header=None)

print("\n🧪 Column Data Types:")
print(df.dtypes)

print("\n🔍 Non-numeric values:")
non_numeric = df.applymap(lambda x: isinstance(x, str) or pd.isnull(x)).any()
print(non_numeric)

print("\n🚨 First few rows:")
print(df.head())

import pandas as pd

df = pd.read_csv("dataset/sample_loan_fixed_for_xgboost.csv", header=None)

print("Sample rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nNull values?")
print(df.isnull().sum())

print("\nValue counts in label (first) column:")
print(df[0].value_counts())

if df.dtypes.apply(lambda x: pd.api.types.is_numeric_dtype(x)).all():
    print("\n✅ All columns are numeric.")
else:
    print("\n❌ Some columns are non-numeric.")

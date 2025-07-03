# clean_sales_data.py

import pandas as pd
import os

# Define paths
input_path = "./dataset/sample_sales_dataset_dirty.csv"
output_path = "./dataset/cleaned_sample_sales_dataset.csv"

# Load dataset
df = pd.read_csv(input_path)

# === Step 5: Data Preview and Basic Exploration ===
print("🔍 Column Names and Types:")
print(df.dtypes)

print("\n📊 Sample Rows:")
print(df.head())

print("\n📈 Summary Statistics for 'PurchaseAmount':")
print(df['PurchaseAmount'].describe())

print("\n🔍 Missing Values by Column:")
print(df.isnull().sum())

# === Step 6: Data Cleaning and Transformation ===

# 1. Impute missing 'Age' values with median
if 'Age' in df.columns:
    median_age = df['Age'].median()
    df['Age'] = df['Age'].fillna(median_age)


# 2. One-hot encode 'Gender' and 'Country'
categorical_cols = ['Gender', 'Country']
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# 3. Rename 'PurchaseAmount' to 'Purchase_Value'
df.rename(columns={'PurchaseAmount': 'Purchase_Value'}, inplace=True)

# Save cleaned dataset
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\n✅ Cleaned dataset saved to: {output_path}")

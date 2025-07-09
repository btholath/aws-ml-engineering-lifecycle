# scripts/clean_batch_input.py
import pandas as pd

# Load the full validation dataset
df = pd.read_csv("/workspaces/aws-ml-engineering-lifecycle/01_data/01_data/validation/sample_realistic_loan_approval_dataset_valid.csv")

# Drop columns that are not needed or are not numeric
columns_to_drop = ['CustomerID', 'label', 'predicted_proba']
df_clean = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Save cleaned CSV
output_path = "/workspaces/aws-ml-engineering-lifecycle/01_data/01_data/validation/batch_input_clean.csv"
df_clean.to_csv(output_path, index=False, header=False)

print(f"✅ Cleaned batch input saved to: {output_path}")


"""
Next run following commands:

Then upload the cleaned file to your S3 bucket:
aws s3 cp /workspaces/aws-ml-engineering-lifecycle/01_data/01_data/validation/batch_input_clean.csv s3://btholath-sagemaker-datawrangler-demo/data/inference/


Update your .env:
XGB_BATCH_INPUT=s3://btholath-sagemaker-datawrangler-demo/data/inference/batch_input_clean.csv

Then rerun your pipeline:
./05_model_inference/run_inference_pipeline.sh
"""
# Script: 3_setup_data_wrangler_flow.py
# Purpose: Guide user to open SageMaker Data Wrangler flow and import S3 data

bucket_name = 'your-existing-or-created-bucket-name'
s3_uri = f"s3://{bucket_name}/data/cleaned_sample_sales_dataset.csv"

def guide_data_wrangler_ingestion():
    print("\n🚀 ACTION REQUIRED:")
    print("1. Open SageMaker Studio in your AWS Console.")
    print("2. Launch a new Data Wrangler Flow.")
    print(f"3. Import data from S3 URI: {s3_uri}")
    print("4. Perform basic transformations, profiling, and export to S3.")

if __name__ == "__main__":
    guide_data_wrangler_ingestion()

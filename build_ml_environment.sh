#!/bin/bash
set -e
set -o pipefail

echo "🧹 Cleaning up old SageMaker Studio domain (if exists)..."

# Delete SageMaker Studio domain if it exists
REGION=$(aws configure get region)
DOMAIN_NAME=$(aws sagemaker list-domains --region $REGION --query "Domains[0].DomainName" --output text)

if [ "$DOMAIN_NAME" != "None" ]; then
  echo "⚠️  Found existing Studio Domain: $DOMAIN_NAME. Deleting..."
  DOMAIN_ID=$(aws sagemaker list-domains --region $REGION --query "Domains[0].DomainId" --output text)
  
  # Delete user profiles under the domain
  USER_PROFILES=$(aws sagemaker list-user-profiles --domain-id-equals "$DOMAIN_ID" --region $REGION --query "UserProfiles[].UserProfileName" --output text)

  for PROFILE in $USER_PROFILES; do
    echo "🧽 Deleting user profile: $PROFILE"
    aws sagemaker delete-user-profile --domain-id "$DOMAIN_ID" --user-profile-name "$PROFILE" --region $REGION
  done

  # Delete the domain
  aws sagemaker delete-domain --domain-id "$DOMAIN_ID" --region $REGION --no-retain-deployment-type
  echo "✅ SageMaker Studio Domain deleted: $DOMAIN_NAME"
else
  echo "ℹ️ No existing SageMaker Studio domain found."
fi

echo "🚀 Starting ML environment setup..."

# Step 1: Infrastructure
cd 00_infrastructure
./create_all_resources.sh
cd ..

# Step 2: Data transformation
echo "🧹 [02] Running transformation steps..."
cd 02_data_preparation/transform
./run_all_transform_steps.sh  # Generates processed files
cd ../../

# Step 3: Data splitting (needs ready.csv from above step)
echo "📊 [01] Preparing raw data..."
cd 01_data
python scripts/02_split_validation_data.py
python scripts/03_transform_data.py
python scripts/04_upload_cleaned_to_s3.py
cd ..

# Step 4: Feature Store
echo "📊 [03] Creating and ingesting feature store groups..."
cd 02_data_preparation/feature_store
./run_all_feature_store_steps.sh
cd ../../

echo "✅ ML environment setup completed successfully."

#!/bin/bash
set -e
set -o pipefail

REGION=$(aws configure get region)
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

echo "🔻 Deleting all AWS ML project resources in region: $REGION"

# 1. Delete SageMaker Studio Domain and User Profiles
echo "🧹 Checking for SageMaker Studio domain..."
DOMAIN_ID=$(aws sagemaker list-domains --region "$REGION" --query "Domains[0].DomainId" --output text)

if [ "$DOMAIN_ID" != "None" ]; then
  USER_PROFILES=$(aws sagemaker list-user-profiles --region "$REGION" --domain-id-equals "$DOMAIN_ID" --query "UserProfiles[].UserProfileName" --output text)

  for PROFILE in $USER_PROFILES; do
    echo "🧽 Deleting user profile: $PROFILE"
    aws sagemaker delete-user-profile --region "$REGION" --domain-id "$DOMAIN_ID" --user-profile-name "$PROFILE"
  done

  echo "❌ Deleting Studio domain: $DOMAIN_ID"
  aws sagemaker delete-domain --region "$REGION" --domain-id "$DOMAIN_ID"
else
  echo "✅ No Studio domain found."
fi

# 2. Delete all SageMaker endpoints
echo "🧼 Deleting SageMaker endpoints..."
ENDPOINTS=$(aws sagemaker list-endpoints --region "$REGION" --query "Endpoints[].EndpointName" --output text)
for EP in $ENDPOINTS; do
  echo "❌ Deleting endpoint: $EP"
  aws sagemaker delete-endpoint --region "$REGION" --endpoint-name "$EP"
done

# 3. Delete all SageMaker models
echo "🧼 Deleting SageMaker models..."
MODELS=$(aws sagemaker list-models --region "$REGION" --query "Models[].ModelName" --output text)
for MODEL in $MODELS; do
  echo "❌ Deleting model: $MODEL"
  aws sagemaker delete-model --region "$REGION" --model-name "$MODEL"
done

# 4. Delete model packages
echo "🧼 Deleting SageMaker model packages..."
MODEL_PACKAGES=$(aws sagemaker list-model-packages --region "$REGION" --query "ModelPackageSummaryList[].ModelPackageArn" --output text)
for MP in $MODEL_PACKAGES; do
  echo "❌ Deleting model package: $MP"
  aws sagemaker delete-model-package --region "$REGION" --model-package-name "$MP"
done

# 5. Delete model package groups
echo "🧼 Deleting model package groups..."
PACKAGE_GROUPS=$(aws sagemaker list-model-package-groups --region "$REGION" --query "ModelPackageGroupSummaryList[].ModelPackageGroupName" --output text)
for PG in $PACKAGE_GROUPS; do
  echo "❌ Deleting model package group: $PG"
  aws sagemaker delete-model-package-group --region "$REGION" --model-package-group-name "$PG"
done

# 6. Delete Feature Store groups
echo "🧼 Deleting SageMaker Feature Groups..."
FEATURE_GROUPS=$(aws sagemaker list-feature-groups --region "$REGION" --query "FeatureGroupSummaries[].FeatureGroupName" --output text)
for FG in $FEATURE_GROUPS; do
  echo "❌ Deleting feature group: $FG"
  aws sagemaker delete-feature-group --region "$REGION" --feature-group-name "$FG"
done

# 7. Delete S3 bucket contents (optional)
echo "🪣 Cleaning S3 buckets (prompted)..."
read -p "Do you want to delete ALL contents of your project S3 buckets (y/N)? " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
    buckets=$(aws s3api list-buckets --query "Buckets[].Name" --output text)
    for bucket in $buckets; do
        echo "❌ Deleting contents of bucket: $bucket"
        aws s3 rm "s3://$bucket" --recursive
    done
else
    echo "🟡 Skipping S3 bucket cleanup."
fi


# 8. Detach and delete IAM Role
ROLE_NAME="AmazonSageMakerExecutionRole"
echo "🔐 Checking IAM role: $ROLE_NAME"
aws iam detach-role-policy --role-name "$ROLE_NAME" --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess || true
aws iam delete-role --role-name "$ROLE_NAME" && echo "✅ Deleted IAM role $ROLE_NAME" || echo "⚠️ Could not delete IAM role (in use?)"

# 9. (Optional) Delete security group / VPC
# Uncomment if you know the IDs
# aws ec2 delete-security-group --group-id sg-xxxxxxxx
# aws ec2 delete-subnet --subnet-id subnet-xxxxxxxx
# aws ec2 delete-vpc --vpc-id vpc-xxxxxxxx

echo "🎉 All major AWS resources deleted successfully."

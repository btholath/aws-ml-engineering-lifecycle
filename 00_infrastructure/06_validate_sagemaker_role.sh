#!/bin/bash

# Load from .env (must be in project root)
source "$(dirname "$0")/../.env"

ROLE_NAME=$(basename "$SAGEMAKER_ROLE_ARN")
echo "🔍 Validating role: $ROLE_NAME"

echo "----------------------------------------"
echo "1️⃣ Checking IAM role exists..."
aws iam get-role --role-name "$ROLE_NAME" >/dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ IAM role exists: $ROLE_NAME"
else
  echo "❌ IAM role not found: $ROLE_NAME"
  exit 1
fi

echo "----------------------------------------"
echo "2️⃣ Simulating IAM permissions (ListBuckets, CreateTrainingJob)..."
aws iam simulate-principal-policy \
  --policy-source-arn "$SAGEMAKER_ROLE_ARN" \
  --action-names "s3:ListBucket" "sagemaker:CreateTrainingJob" "logs:CreateLogStream" "logs:PutLogEvents" \
  --output table

echo "----------------------------------------"
echo "3️⃣ Verifying inline or attached policies..."
aws iam list-attached-role-policies --role-name "$ROLE_NAME" --output table

echo "----------------------------------------"
echo "✅ Role validation completed."
echo "If any permissions are missing, attach AmazonSageMakerFullAccess:"
echo "aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"

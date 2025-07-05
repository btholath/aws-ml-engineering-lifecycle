#!/bin/bash

# Define role name
ROLE_NAME="AmazonSageMakerExecutionRole"

# Trust policy for SageMaker
TRUST_POLICY='{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sagemaker.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}'

# Create the role
echo "🚀 Creating SageMaker execution role: $ROLE_NAME..."
aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document "$TRUST_POLICY" > /dev/null

# Attach full SageMaker access policy
echo "🔐 Attaching AmazonSageMakerFullAccess..."
aws iam attach-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

# Get the role ARN
ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)

# Append to .env
if [ -f "../.env" ]; then
  echo "SAGEMAKER_ROLE_ARN=$ROLE_ARN" >> ../.env
  echo "✅ .env file updated with: $ROLE_ARN"
else
  echo "⚠️  .env not found. Please manually add:"
  echo "SAGEMAKER_ROLE_ARN=$ROLE_ARN"
fi

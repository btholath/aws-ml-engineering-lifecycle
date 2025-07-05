#!/bin/bash
# This script attaches a policy to the SageMaker Execution Role

source "$(dirname "$0")/../.env"

ROLE_NAME=$(echo "$SAGEMAKER_ROLE_ARN" | cut -d'/' -f2)

echo "ℹ️ Attaching AmazonSageMakerFullAccess to role: $ROLE_NAME"

aws iam attach-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

echo "✅ Role updated: $SAGEMAKER_ROLE_ARN"

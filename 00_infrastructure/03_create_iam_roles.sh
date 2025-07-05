#!/bin/bash
# This script assumes that the IAM role already exists.
# It attaches a policy to the existing SageMaker Execution Role if needed.

source "$(dirname "$0")/../.env"


echo "ℹ️ Attaching AmazonSageMakerFullAccess to role: $SAGEMAKER_ROLE_ARN"
aws iam attach-role-policy \\
    --role-name "$(basename $SAGEMAKER_ROLE_ARN)" \\
    --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

echo "✅ Role updated: $SAGEMAKER_ROLE_ARN"
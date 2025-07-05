#!/bin/bash
# Check if the main resources exist

source "$(dirname "$0")/../.env"


echo "🔍 Checking S3 bucket..."
aws s3 ls "s3://$S3_BUCKET"

echo "🔍 Checking SageMaker domains..."
aws sagemaker list-domains --region "$AWS_REGION"

echo "🔍 Checking IAM Role..."
aws iam get-role --role-name "$(basename $SAGEMAKER_ROLE_ARN)"
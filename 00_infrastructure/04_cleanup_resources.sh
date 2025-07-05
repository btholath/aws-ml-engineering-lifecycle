#!/bin/bash
# Delete SageMaker domain and S3 bucket (use with caution!)

source "$(dirname "$0")/../.env"


DOMAIN_NAME="sagemaker-studio-domain"

echo "🗑️ Deleting SageMaker domain..."
aws sagemaker delete-domain --domain-id \\
    $(aws sagemaker list-domains --region "$AWS_REGION" --query "Domains[?DomainName=='$DOMAIN_NAME'].DomainId" --output text)

echo "🗑️ Emptying and deleting S3 bucket..."
aws s3 rm s3://$S3_BUCKET --recursive
aws s3api delete-bucket --bucket $S3_BUCKET

echo "✅ Cleanup complete."
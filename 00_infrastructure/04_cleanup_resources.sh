#!/bin/bash

source "$(dirname "$0")/../.env"

DOMAIN_NAME="sagemaker-studio-domain"

# Get Domain ID by name
DOMAIN_ID=$(aws sagemaker list-domains --region "$AWS_REGION" \
  --query "Domains[?DomainName=='$DOMAIN_NAME'].DomainId" --output text)

echo "🗑️ Deleting SageMaker domain..."
if [[ -n "$DOMAIN_ID" && "$DOMAIN_ID" == d-* ]]; then
    aws sagemaker delete-domain \
        --domain-id "$DOMAIN_ID" \
        --region "$AWS_REGION"
    echo "✅ Domain deleted: $DOMAIN_ID"
else
    echo "❌ Could not resolve valid domain ID for '$DOMAIN_NAME'. Skipping deletion."
fi

# Delete S3 contents and bucket
echo "🗑️ Emptying and deleting S3 bucket..."
aws s3 rm "s3://$S3_BUCKET" --recursive
aws s3api delete-bucket --bucket "$S3_BUCKET"

echo "✅ Cleanup complete."

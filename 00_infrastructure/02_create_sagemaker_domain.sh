#!/bin/bash
# Create a SageMaker Studio domain

source "$(dirname "$0")/../.env"

DOMAIN_NAME="sagemaker-studio-domain"
USER_PROFILE_NAME="studio-user"

# Check if domain exists
DOMAIN_EXISTS=$(aws sagemaker list-domains --region "$AWS_REGION" | grep "$DOMAIN_NAME")

if [[ -z "$DOMAIN_EXISTS" ]]; then
    echo "🚀 Creating SageMaker Studio domain..."

    aws sagemaker create-domain \
        --domain-name "$DOMAIN_NAME" \
        --region "$AWS_REGION" \
        --vpc-id "$VPC_ID" \
        --subnet-ids $(echo $SUBNET_IDS | tr ',' ' ') \
        --auth-mode IAM \
        --app-network-access-type PublicInternetOnly \
        --default-user-settings ExecutionRole="$SAGEMAKER_ROLE_ARN"

    echo "✅ SageMaker Studio domain creation initiated: $DOMAIN_NAME"
else
    echo "⚠️  SageMaker domain already exists: $DOMAIN_NAME"
fi

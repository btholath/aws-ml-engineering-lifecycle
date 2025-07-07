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

# Fetch Domain ID
DOMAIN_ID=$(aws sagemaker list-domains --query "Domains[?DomainName=='$DOMAIN_NAME'].DomainId" --output text --region "$REGION")

# Check if user profile exists
USER_PROFILE_EXISTS=$(aws sagemaker list-user-profiles --domain-id-equals "$DOMAIN_ID" --query "UserProfiles[?UserProfileName=='$USER_PROFILE_NAME'] | length(@)" --output text --region "$REGION")

if [[ "$USER_PROFILE_EXISTS" == "0" ]]; then
    echo "👤 Creating user profile: $USER_PROFILE_NAME"
    aws sagemaker create-user-profile \
      --domain-id "$DOMAIN_ID" \
      --user-profile-name "$USER_PROFILE_NAME" \
      --user-settings "ExecutionRole=$ROLE_ARN" \
      --region "$REGION"
    echo "✅ User profile created: $USER_PROFILE_NAME"
else
    echo "ℹ️ User profile already exists: $USER_PROFILE_NAME"
fi
#!/bin/bash

VPC_ID="vpc-0fd72d7ba68e578d2"
SG_NAME="sagemaker-studio-sg"
DESCRIPTION="Security Group for SageMaker Studio access"

# Create security group
SG_ID=$(aws ec2 create-security-group \
    --group-name "$SG_NAME" \
    --description "$DESCRIPTION" \
    --vpc-id "$VPC_ID" \
    --query 'GroupId' \
    --output text)

echo "✅ Created Security Group: $SG_ID"

# Authorize outbound traffic
aws ec2 authorize-security-group-egress \
    --group-id "$SG_ID" \
    --protocol "-1" \
    --port all \
    --cidr 0.0.0.0/0

echo "🌐 Allowed all outbound traffic from $SG_ID"

# Print result
echo "🔐 SECURITY_GROUP_ID=$SG_ID"

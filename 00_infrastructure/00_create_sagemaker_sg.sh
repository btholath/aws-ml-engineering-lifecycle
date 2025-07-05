#!/bin/bash

# Load environment
source "$(dirname "$0")/../.env"

VPC_ID=${VPC_ID}
SG_NAME="sagemaker-studio-sg"
DESCRIPTION="Security Group for SageMaker Studio access"

# Check if the SG already exists
SG_ID=$(aws ec2 describe-security-groups \
  --filters Name=group-name,Values="$SG_NAME" Name=vpc-id,Values="$VPC_ID" \
  --query "SecurityGroups[0].GroupId" \
  --output text)

if [[ "$SG_ID" == "None" || -z "$SG_ID" ]]; then
  echo "✅ Creating new Security Group: $SG_NAME"
  SG_ID=$(aws ec2 create-security-group \
    --group-name "$SG_NAME" \
    --description "$DESCRIPTION" \
    --vpc-id "$VPC_ID" \
    --query 'GroupId' \
    --output text)
else
  echo "ℹ️ Security group already exists: $SG_NAME ($SG_ID)"
fi

# Check if outbound rule already exists
rule_exists=$(aws ec2 describe-security-groups \
  --group-ids "$SG_ID" \
  --query "SecurityGroups[0].IpPermissionsEgress[?IpRanges[?CidrIp=='0.0.0.0/0']]" \
  --output text)

if [[ -z "$rule_exists" ]]; then
  echo "🌐 Adding outbound rule to $SG_ID"
  aws ec2 authorize-security-group-egress \
    --group-id "$SG_ID" \
    --protocol "-1" \
    --port all \
    --cidr 0.0.0.0/0
else
  echo "🌐 Outbound rule already exists for $SG_ID"
fi

echo "🔐 SECURITY_GROUP_ID=$SG_ID"

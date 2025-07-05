#!/bin/bash

source "$(dirname "$0")/../.env"

BUCKET_NAME="$S3_BUCKET"
REGION="$AWS_REGION"

echo "🚀 Creating bucket $BUCKET_NAME in region $REGION..."

# Check if the bucket already exists
if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
  echo "⚠️  Bucket already exists: $BUCKET_NAME"
else
  if [ "$REGION" == "us-east-1" ]; then
    aws s3api create-bucket --bucket "$BUCKET_NAME" --region "$REGION"
  else
    aws s3api create-bucket \
      --bucket "$BUCKET_NAME" \
      --region "$REGION" \
      --create-bucket-configuration LocationConstraint="$REGION"
  fi
  echo "✅ Bucket created: $BUCKET_NAME"
fi

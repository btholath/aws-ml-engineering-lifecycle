#!/bin/bash
# Creates the S3 bucket if it does not already exist

source "$(dirname "$0")/../.env"


if aws s3api head-bucket --bucket "$S3_BUCKET" 2>/dev/null; then
    echo "⚠️  Bucket $S3_BUCKET already exists."
else
    echo "🚀 Creating bucket $S3_BUCKET in region $AWS_REGION..."
    aws s3api create-bucket --bucket "$S3_BUCKET" --create-bucket-configuration LocationConstraint=$AWS_REGION
    echo "✅ Bucket created: $S3_BUCKET"
fi
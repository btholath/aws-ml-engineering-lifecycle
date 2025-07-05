#!/bin/bash
set -e

echo "🛠️ Creating SageMaker execution role..."
./00_create_sagemaker_execution_role.sh

echo "🌐 Creating SageMaker security group..."
./00_create_sagemaker_sg.sh

echo "🪣 Creating S3 bucket..."
./01_create_s3_bucket.sh

echo "🧠 Launching SageMaker Studio domain..."
./02_create_sagemaker_domain.sh

echo "🔐 Attaching IAM policies..."
./03_create_iam_roles.sh

echo "✅ Validating IAM role permissions..."
./06_validate_sagemaker_role.sh

echo "✅ All AWS resources created successfully."

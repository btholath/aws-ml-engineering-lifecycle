#!/bin/bash

source "$(dirname "$0")/../.env"

echo "🧠 Deleting all SageMaker endpoints..."
for endpoint in $(aws sagemaker list-endpoints --query "Endpoints[*].EndpointName" --output text --region "$AWS_REGION"); do
  echo "❌ Deleting endpoint: $endpoint"
  aws sagemaker delete-endpoint --endpoint-name "$endpoint" --region "$AWS_REGION"
done

echo "📦 Deleting all SageMaker models..."
for model in $(aws sagemaker list-models --query "Models[*].ModelName" --output text --region "$AWS_REGION"); do
  echo "❌ Deleting model: $model"
  aws sagemaker delete-model --model-name "$model" --region "$AWS_REGION"
done

echo "🔄 Deleting model packages in group: $MODEL_PACKAGE_GROUP"
package_arns=$(aws sagemaker list-model-packages \
  --model-package-group-name "$MODEL_PACKAGE_GROUP" \
  --query "ModelPackageSummaryList[*].ModelPackageArn" \
  --output text \
  --region "$AWS_REGION")

for arn in $package_arns; do
  echo "❌ Deleting model package: $arn"
  aws sagemaker delete-model-package --model-package-name "$arn" --region "$AWS_REGION"
done

echo "🧹 Deleting model package group (if exists)..."
aws sagemaker delete-model-package-group \
  --model-package-group-name "$MODEL_PACKAGE_GROUP" \
  --region "$AWS_REGION" 2>/dev/null || echo "⚠️ Group may already be deleted."

echo "🔐 Detaching all policies from SageMaker role..."
ROLE_NAME=$(echo "$SAGEMAKER_ROLE_ARN" | cut -d'/' -f2)

attached_policies=$(aws iam list-attached-role-policies --role-name "$ROLE_NAME" \
  --query 'AttachedPolicies[*].PolicyArn' --output text)

for policy in $attached_policies; do
  echo "❌ Detaching policy: $policy"
  aws iam detach-role-policy --role-name "$ROLE_NAME" --policy-arn "$policy"
done

echo "🛑 Deleting IAM role (optional)..."
read -p "❓ Delete IAM role $ROLE_NAME? (y/n): " confirm
if [[ "$confirm" == "y" ]]; then
  aws iam delete-role --role-name "$ROLE_NAME"
  echo "✅ IAM role deleted: $ROLE_NAME"
else
  echo "⏭️ Skipping IAM role deletion."
fi

echo "✅ Full SageMaker environment cleanup complete."

import boto3
import time

sagemaker = boto3.client("sagemaker", region_name="us-east-1")

model_package_group_name = "LoanApprovalModelGroup"
model_name = "real-loan-predictor-xgb-1751671461"
model_artifact = "s3://btholath-sagemaker-datawrangler-demo/None/real-loan-predictor-xgb-1751671461/output/model.tar.gz"

# Create Model Package Group (if not exists)
try:
    sagemaker.create_model_package_group(
        ModelPackageGroupName=model_package_group_name,
        ModelPackageGroupDescription="Loan approval prediction models"
    )
except sagemaker.exceptions.ResourceInUse:
    pass  # Already exists

# Register model
response = sagemaker.create_model_package(
    ModelPackageGroupName=model_package_group_name,
    ModelPackageDescription="XGBoost loan predictor",
    InferenceSpecification={
        "Containers": [{
            "Image": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1",
            "ModelDataUrl": model_artifact
        }],
        "SupportedContentTypes": ["text/csv"],
        "SupportedResponseMIMETypes": ["text/csv"]
    },
    ModelApprovalStatus="PendingManualApproval"
)

print(f"✅ Model registered: {response['ModelPackageArn']}")

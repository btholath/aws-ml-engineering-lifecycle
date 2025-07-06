```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
sudo apt update

aws configure
AWS Access Key ID [None]: ....
AWS Secret Access Key [None]: ....
Default region name [None]: ....
Default output format [None]: json
```

----------
***one-time setup of folder structure***
```bash
@btholath ➜ /workspaces $ chmod +x aws-ml-engineering-lifecycle/onetime_generate_project_structure.sh
@btholath ➜ /workspaces $ ./aws-ml-engineering-lifecycle/onetime_generate_project_structure.sh
```

***Create and execute scriptes in 00_infrastructure**
cd /workspaces/aws-ml-engineering-lifecycle/00_infrastructure
chmod +x 00_create_sagemaker_sg.sh
chmod +x 00_create_sagemaker_execution_role.sh
chmod +x 01_create_s3_bucket.sh
chmod +x 02_create_sagemaker_domain.sh
chmod +x 03_create_iam_roles.sh
chmod +x 04_cleanup_resources.sh
chmod +x 05_check_resource_status.sh
chmod +x 06_validate_sagemaker_role.sh

***Create AWS resources***
create_all_resources.sh

***Delete AWS resources***
aws sagemaker list-feature-groups --region us-east-1

aws sagemaker describe-feature-group \
  --feature-group-name loan-approval-feature-group \
  --region us-east-1

aws sagemaker describe-feature-group \
  --feature-group-name loan-approval-feature-group \
  --region us-east-1 \
  --query 'FeatureGroupStatus'

aws s3 ls s3://btholath-sagemaker-datawrangler-demo/feature-store/
aws s3 cp s3://btholath-sagemaker-datawrangler-demo/feature-store/your_file.parquet ./local.parquet

aws sagemaker delete-feature-group --feature-group-name loan-approval-feature-group --region us-east-1

aws s3 cp s3://btholath-sagemaker-datawrangler-demo/data/sample_realistic_loan_approval_dataset_ready.csv \
          s3://btholath-sagemaker-datawrangler-demo/data/validation/sample_realistic_loan_approval_dataset_ready.csv


@btholath ➜ /workspaces/aws-ml-engineering-lifecycle/00_infrastructure (main) $ chmod +x ./02_create_sagemaker_domain.sh
🚀 Creating SageMaker Studio domain...
{
    "DomainArn": "arn:aws:sagemaker:us-east-1:637423309379:domain/d-urjdcehn8mid",
    "DomainId": "d-urjdcehn8mid",
    "Url": "https://d-urjdcehn8mid.studio.us-east-1.sagemaker.aws"
}
✅ SageMaker Studio domain creation initiated: sagemaker-studio-domain

https://d-urjdcehn8mid.studio.us-east-1.sagemaker.aws

@btholath ➜ /workspaces/aws-ml-engineering-lifecycle/00_infrastructure (main) $ 


@btholath ➜ /workspaces/aws-ml-engineering-lifecycle/00_infrastructure (main) $ ./03_create_iam_roles.sh
ℹ️ Attaching AmazonSageMakerFullAccess to role: AmazonSageMakerExecutionRole
✅ Role updated: arn:aws:iam::637423309379:role/AmazonSageMakerExecutionRole


@btholath ➜ /workspaces/aws-ml-engineering-lifecycle/00_infrastructure (main) $ ./04_cleanup_resources.sh


./05_check_resource_status.sh

./06_validate_sagemaker_role.sh

*** organize the natural execution flow of the scripts in 02_data_preparation/ based on the machine learning lifecycle and dependencies between stages.***
Recommended Execution Order (with Reasoning)
1️⃣ data_wrangler/ – Visual Data Preparation (Optional but GUI-friendly)
Use this if you're preparing your dataset visually in SageMaker Studio.

Execution Order:

Step	Script	Purpose
1	01_generate_flow.py	Programmatically generate a .flow file with transform steps (impute, encode, rename, etc.)
2	02_upload_flow.py	Upload the .flow to S3 so SageMaker Studio can import it
3	(In Studio)	Use SageMaker Data Wrangler UI to apply, explore, export
–	template.flow	Template or auto-generated file

🔄 Optional: Use only if you prefer Data Wrangler GUI to generate the final transformed dataset.

2️⃣ transform/ – Programmatic Data Cleaning Pipeline
Use this path for fully scripted data prep (ideal for reproducibility and automation).

Execution Order:

Step	Script	Purpose
1	01_clean_data.py	Handle missing values, normalize numerics
2	02_encode_features.py	One-hot encode categorical variables (e.g., Gender, EducationLevel)
3	03_fix_booleans_and_upload.py	Convert TRUE/FALSE to 1/0, rename LoanApproved → label, upload to S3
4	04_validate_dataset.py	Check for schema validity, data types, nulls
5	05_generate_statistics.py	Basic statistics, distributions, for visualization & QC

🔁 This is your main path if you're training using XGBoost or scripts (not Studio GUI).

3️⃣ feature_store/ – Advanced Option: Feature Reuse / Monitoring
Use this if you're managing features across multiple models or teams.

Execution Order:

Step	Script	Purpose
1	01_create_feature_group.py	Create SageMaker Feature Group (defines schema, keys, etc.)
2	02_ingest_features.py	Ingest features into the group from a DataFrame or CSV

🧠 Use after data is cleaned and transformed (i.e., after transform/03_fix_booleans_and_upload.py).

🔁 Final Workflow Recommendation
# For most automation pipelines (non-GUI):

02_data_preparation/transform/
├── 01_clean_data.py
├── 02_encode_features.py
├── 03_fix_booleans_and_upload.py
├── 04_validate_dataset.py
├── 05_generate_statistics.py

# Optional:
02_data_preparation/data_wrangler/
├── 01_generate_flow.py
├── 02_upload_flow.py

# Optional (advanced MLOps):
02_data_preparation/feature_store/
├── 01_create_feature_group.py
├── 02_ingest_features.py


END-OF_TASKS
----------

```bash
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/build_dataset/gen_home_sales_dataset.py 
Dataset generated and saved as ./dataset/sample_home_sales_dataset.csv
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/build_dataset/gen_loan_approval_dataset.py 
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/build_dataset/gen_sales_dataset.py 
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/build_dataset/gen_large_datset.py 
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/build_dataset/gen_realistic_loan_approval_dataset.py 
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 
```

```bash
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/transform/clean_sales_data.py 
🔍 Column Names and Types:
CustomerID         object
Age               float64
Gender             object
Product            object
PurchaseAmount    float64
Country            object
dtype: object

📊 Sample Rows:
  CustomerID   Age       Gender     Product  PurchaseAmount       Country
0  CUST00001  39.0         Male      Camera          278.05            UK
1  CUST00002  27.0  Unspecified       Mouse          923.75        Canada
2  CUST00003  62.0       Female      Tablet          455.07        Canada
3  CUST00004  66.0         Male     Monitor         2543.36  South Africa
4  CUST00005  76.0  Unspecified  Smartwatch         2798.06  South Africa

📈 Summary Statistics for 'PurchaseAmount':
count    5000.000000
mean     1532.072220
std       859.499178
min        20.370000
25%       803.042500
50%      1549.010000
75%      2287.152500
max      2999.930000
Name: PurchaseAmount, dtype: float64

🔍 Missing Values by Column:
CustomerID         0
Age               14
Gender             0
Product            0
PurchaseAmount     0
Country            0
dtype: int64

✅ Cleaned dataset saved to: ./dataset/cleaned_sample_sales_dataset.csv
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 
```

** Upload dataset to S3 **
```bash
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle/dataset (main) $ aws s3 sync . s3://btholath-sagemaker-datawrangler-demo/data/
upload: ./sample_loan_approval_dataset.csv to s3://btholath-sagemaker-datawrangler-demo/data/sample_loan_approval_dataset.csv
upload: ./sample_sales_dataset_dirty.csv to s3://btholath-sagemaker-datawrangler-demo/data/sample_sales_dataset_dirty.csv
upload: ./sample_loan_approval_dataset_dirty.csv to s3://btholath-sagemaker-datawrangler-demo/data/sample_loan_approval_dataset_dirty.csv
upload: ./sample_sales_dataset.csv to s3://btholath-sagemaker-datawrangler-demo/data/sample_sales_dataset.csv
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle/dataset (main) $ 
```


** Ingest **
```bash
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/ingest/1_create_resources.py 
2025-07-03 17:02:30,235 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-03 17:02:30,832 [INFO] ✅ Created S3 bucket: btholath-sagemaker-datawrangler-demo
2025-07-03 17:02:31,173 [WARNING] ❗ No SageMaker Studio domains found.
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $
```

(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/data_wrangler/upload_data_wrangler_flow.py 
2025-07-03 17:05:33,537 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-03 17:05:33,952 [INFO] ✅ Uploaded .flow to s3://btholath-sagemaker-datawrangler-demo/data-wrangler/flows/customer_sales_cleaning.flow
2025-07-03 17:05:33,952 [INFO] 
📌 MANUAL STEP REQUIRED:
2025-07-03 17:05:33,952 [INFO] 1. Go to SageMaker Studio.
2025-07-03 17:05:33,952 [INFO] 2. Open Data Wrangler → 'Import Flow'.
2025-07-03 17:05:33,952 [INFO] 3. Select: s3://btholath-sagemaker-datawrangler-demo/data-wrangler/flows/customer_sales_cleaning.flow
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 

(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/data_wrangler/patch_flow_template.py 
2025-07-03 17:33:57,350 [INFO] ✅ Patched .flow file saved: 01_data_preparation/data_wrangler/customer_sales_cleaning.flow
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 


(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/ingest/2_upload_dataset.py
✅ Uploaded /workspaces/aws-ml-engineering-lifecycle/dataset/cleaned_sample_sales_dataset.csv to s3://btholath-sagemaker-datawrangler-demo/data/cleaned_sample_sales_dataset.csv


(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/ingest/3_setup_data_wrangler_flow.py

🚀 ACTION REQUIRED:
1. Open SageMaker Studio in your AWS Console.
2. Launch a new Data Wrangler Flow.
3. Import data from S3 URI: s3://btholath-sagemaker-datawrangler-demo/data/cleaned_sample_sales_dataset.csv
4. Perform basic transformations, profiling, and export to S3.
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 


***Configuring Data for SageMaker Training Jobs***
```bash
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation//build_dataset/gen_realistic_loan_approval_dataset.py

(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation//build_dataset/csv_to_parquet.py dataset/sample_realistic_loan_approval_dataset.csv
Input file: dataset/sample_realistic_loan_approval_dataset.csv
Output file: dataset/sample_realistic_loan_approval_dataset.parquet
Derived Schema:
CustomerID: string
Age: int64
Gender: string
EducationLevel: string
Income: double
LoanApproved: bool
-- schema metadata --
pandas: '{"index_columns": [{"kind": "range", "name": null, "start": 0, "' + 957
(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 

(.venv) @btholath ➜ /workspaces/aws-ml-engineering-lifecycle/dataset (main) $ aws s3 sync . s3://btholath-sagemaker-datawrangler-demo/data/
upload: ./sample_realistic_loan_approval_dataset.parquet to s3://btholath-sagemaker-datawrangler-demo/data/sample_realistic_loan_approval_dataset.parquet
upload: ./sample_loan_approval_dataset.csv to s3://btholath-sagemaker-datawrangler-demo/data/sample_loan_approval_dataset.csv
upload: ./sample_sales_dataset.csv to s3://btholath-sagemaker-datawrangler-demo/data/sample_sales_dataset.csv
upload: ./sample_loan_approval_dataset_dirty.csv to s3://btholath-sagemaker-datawrangler-demo/data/sample_loan_approval_dataset_dirty.csv
upload: ./sample_sales_dataset_dirty.csv to s3://btholath-sagemaker-datawrangler-demo/data/sample_sales_dataset_dirty.csv
upload: ./sample_realistic_loan_approval_dataset.csv to s3://btholath-sagemaker-datawrangler-demo/data/sample_realistic_loan_approval_dataset.csv
upload: ./cleaned_sample_sales_dataset.csv to s3://btholath-sagemaker-datawrangler-demo/data/cleaned_sample_sales_dataset.csv
```

***Preprocess the CSV for SageMaker Training***
Current sample records in "sample_realistic_loan_approval_dataset.csv"
CustomerID	Age	Gender	EducationLevel	Income	LoanApproved
CUST00001	37	Female	Master's Degree	51887.99	TRUE
CUST00002	21	Unspecified	High School	148757.07	FALSE
CUST00003	80	Unspecified	Associate Degree	149022.46	FALSE
CUST00004	42	Male	Associate Degree	131774.59	FALSE

The prepare_csv_for_xgboost.py will do the following, before we can use the CSV file for SageMaker training.
Loads your dataset
Encodes categorical variables
Converts LoanApproved TRUE/FALSE → 1/0
Moves label column to the front
Drops headers and saves in numeric-only format
Uploads the file to S3

@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/transform/prepare_loan_dataset_for_xgboost.py
2025-07-04 22:53:16,636 [INFO] ✅ CSV ready for XGBoost: ./dataset/sample_loan_ready_for_xgboost.csv
2025-07-04 22:53:16,647 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-04 22:53:17,296 [INFO] 📤 Uploaded to S3: s3://btholath-sagemaker-datawrangler-demo/data/sample_loan_ready_for_xgboost.csv
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 


***Run the training job***
```bash
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/transform/troubleshoot_dataset.py 

🧪 Column Data Types:
0      int64
1      int64
2    float64
3       bool
4       bool
5       bool
6       bool
7       bool
8       bool
dtype: object

🔍 Non-numeric values:
/workspaces/aws-ml-engineering-lifecycle/01_data_preparation/transform/troubleshoot_dataset.py:9: FutureWarning: DataFrame.applymap has been deprecated. Use DataFrame.map instead.
  non_numeric = df.applymap(lambda x: isinstance(x, str) or pd.isnull(x)).any()
0    False
1    False
2    False
3    False
4    False
5    False
6    False
7    False
8    False
dtype: bool

🚨 First few rows:
   0   1          2      3      4      5      6      7      8
0  1  37   51887.99  False  False  False  False   True  False
1  0  21  148757.07  False   True  False   True  False  False
2  0  80  149022.46  False   True  False  False  False  False
3  0  42  131774.59   True  False  False  False  False  False
4  0  70  117448.88  False   True  False   True  False  False
```

```bash
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/transform/fix_booleans_and_upload.py 
2025-07-04 23:06:12,845 [INFO] ✅ Fixed and saved: ./dataset/sample_loan_fixed_for_xgboost.csv
2025-07-04 23:06:12,856 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-04 23:06:13,450 [INFO] 📤 Uploaded to: s3://btholath-sagemaker-datawrangler-demo/data/sample_loan_fixed_for_xgboost.csv
```

```bash
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 02_model_training/train_xgboost_loan_predictor.py
sagemaker.config INFO - Not applying SDK defaults from location: /etc/xdg/sagemaker/config.yaml
sagemaker.config INFO - Not applying SDK defaults from location: /home/codespace/.config/sagemaker/config.yaml
2025-07-04 23:07:17,639 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-04 23:07:17,749 [INFO] Ignoring unnecessary instance type: None.
2025-07-04 23:07:17,749 [INFO] Using XGBoost image URI: 683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1
2025-07-04 23:07:17,749 [INFO] Starting SageMaker training job...
2025-07-04 23:07:18,400 [INFO] ✅ Training job created: real-loan-predictor-xgb-1751670437
2025-07-04 23:07:18,400 [INFO] 📦 Output S3 path: s3://btholath-sagemaker-datawrangler-demo/real-loan-predictor-output/
2025-07-04 23:07:18,400 [INFO] 🔗 Job ARN: arn:aws:sagemaker:us-east-1:637423309379:training-job/real-loan-predictor-xgb-1751670437
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 
```

You should be seeing the training job in aws console at https://us-east-1.console.aws.amazon.com/sagemaker/home?region=us-east-1#/jobs
```


@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ head -n 3 dataset/sample_loan_fixed_for_xgboost.csv
1,37,51887.99,0,0,0,0,1,0
0,21,148757.07,0,1,0,1,0,0
0,80,149022.46,0,1,0,0,0,0
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 01_data_preparation/transform/validate_dataset.py 
Sample rows:
   0   1          2  3  4  5  6  7  8
0  1  37   51887.99  0  0  0  0  1  0
1  0  21  148757.07  0  1  0  1  0  0
2  0  80  149022.46  0  1  0  0  0  0
3  0  42  131774.59  1  0  0  0  0  0
4  0  70  117448.88  0  1  0  1  0  0

Data types:
0      int64
1      int64
2    float64
3      int64
4      int64
5      int64
6      int64
7      int64
8      int64
dtype: object

Null values?
0    0
1    0
2    0
3    0
4    0
5    0
6    0
7    0
8    0
dtype: int64

Value counts in label (first) column:
0
1    2997
0    2003
Name: count, dtype: int64

✅ All columns are numeric.
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 


@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 02_model_training/monitor_training_job.py 
⏱️ Status: Completed
✅ Final status: Completed
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 



After training succeeds, 
✅ Monitoring job and fetching logs
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 02_model_training/monitor_training_job.py 
2025-07-04 23:31:51,868 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-04 23:31:52,296 [INFO] Status: Completed
2025-07-04 23:31:52,296 [INFO] Final Status: Completed

✅ Deploying to real-time inference endpoint
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 03_deployment/deploy_model_endpoint.py 
✅ Deployment started. Endpoint name: xgb-loan-model-1751672068-endpoint
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 

✅ Running batch transform on test data
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 03_deployment/batch_transform_job.py
2025-07-04 23:44:32,090 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-04 23:44:32,911 [INFO] ✅ Batch transform job started: xgb-loan-batch-transform-1751672672
2025-07-04 23:44:32,911 [INFO] 📤 Input: s3://btholath-sagemaker-datawrangler-demo/data/sample_loan_fixed_for_xgboost.csv
2025-07-04 23:44:32,911 [INFO] 📁 Output will be saved to: s3://btholath-sagemaker-datawrangler-demo/batch-output/
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 

✅ Registering model in SageMaker Model Registry
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 03_deployment/register_model.py 
✅ Model registered: arn:aws:sagemaker:us-east-1:637423309379:model-package/LoanApprovalModelGroup/1
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 



✅ Automatically approve this model version

✅ Deploy from Model Registry

✅ Compare and promote best models based on evaluation metrics


Run the training job monitor (if you have it set up):

python 03_model_training/02_monitor_training.py
Trigger Hyperparameter Optimization (HPO):


python 03_model_training/hpo/01_run_hpo_job.py
Visualize HPO results:

python 03_model_training/hpo/02_visualize_hpo_results.py
Register model to SageMaker Model Registry (optional):

python 04_model_registry/01_register_model.py
Deploy to a real-time endpoint or run a batch transform job.

-----------------------------------------
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ ./build_ml_environment.sh 
🛠️ Creating SageMaker execution role...
🚀 Creating SageMaker execution role: AmazonSageMakerExecutionRole...

An error occurred (EntityAlreadyExists) when calling the CreateRole operation: Role with name AmazonSageMakerExecutionRole already exists.
🔐 Attaching AmazonSageMakerFullAccess...
✅ .env file updated with: arn:aws:iam::637423309379:role/AmazonSageMakerExecutionRole
🌐 Creating SageMaker security group...
ℹ️ Security group already exists: sagemaker-studio-sg (sg-0d1b3e5aecc6b9e44)
🌐 Outbound rule already exists for sg-0d1b3e5aecc6b9e44
🔐 SECURITY_GROUP_ID=sg-0d1b3e5aecc6b9e44
🪣 Creating S3 bucket...
🚀 Creating bucket btholath-sagemaker-datawrangler-demo in region us-east-1...
{
    "BucketRegion": "us-east-1",
    "AccessPointAlias": false
}
⚠️  Bucket already exists: btholath-sagemaker-datawrangler-demo
🧠 Launching SageMaker Studio domain...
⚠️  SageMaker domain already exists: sagemaker-studio-domain
🔐 Attaching IAM policies...
ℹ️ Attaching AmazonSageMakerFullAccess to role: AmazonSageMakerExecutionRole
✅ Role updated: arn:aws:iam::637423309379:role/AmazonSageMakerExecutionRole
✅ Validating IAM role permissions...
🔍 Validating role: AmazonSageMakerExecutionRole
----------------------------------------
1️⃣ Checking IAM role exists...
✅ IAM role exists: AmazonSageMakerExecutionRole
----------------------------------------
2️⃣ Simulating IAM permissions (ListBuckets, CreateTrainingJob)...
-----------------------------------------------------------------------
|                       SimulatePrincipalPolicy                       |
+---------------------------------------------------------------------+
||                         EvaluationResults                         ||
|+---------------------+-------------------+-------------------------+|
||   EvalActionName    |   EvalDecision    |    EvalResourceName     ||
|+---------------------+-------------------+-------------------------+|
||  s3:ListBucket      |  allowed          |  *                      ||
|+---------------------+-------------------+-------------------------+|
|||                        MatchedStatements                        |||
||+--------------------------------------+--------------------------+||
|||            SourcePolicyId            |    SourcePolicyType      |||
||+--------------------------------------+--------------------------+||
|||  AmazonSageMakerFullAccess           |  IAM Policy              |||
||+--------------------------------------+--------------------------+||
||||                          EndPosition                          ||||
|||+----------------------------------+----------------------------+|||
||||              Column              |           Line             ||||
|||+----------------------------------+----------------------------+|||
||||  4                               |  448                       ||||
|||+----------------------------------+----------------------------+|||
||||                         StartPosition                         ||||
|||+----------------------------------+----------------------------+|||
||||              Column              |           Line             ||||
|||+----------------------------------+----------------------------+|||
||||  4                               |  435                       ||||
|||+----------------------------------+----------------------------+|||
||                         EvaluationResults                         ||
|+------------------------------+---------------+--------------------+|
||        EvalActionName        | EvalDecision  | EvalResourceName   ||
|+------------------------------+---------------+--------------------+|
||  sagemaker:CreateTrainingJob |  allowed      |  *                 ||
|+------------------------------+---------------+--------------------+|
|||                        MatchedStatements                        |||
||+--------------------------------------+--------------------------+||
|||            SourcePolicyId            |    SourcePolicyType      |||
||+--------------------------------------+--------------------------+||
|||  AmazonSageMakerFullAccess           |  IAM Policy              |||
||+--------------------------------------+--------------------------+||
||||                          EndPosition                          ||||
|||+----------------------------------+----------------------------+|||
||||              Column              |           Line             ||||
|||+----------------------------------+----------------------------+|||
||||  4                               |  21                        ||||
|||+----------------------------------+----------------------------+|||
||||                         StartPosition                         ||||
|||+----------------------------------+----------------------------+|||
||||              Column              |           Line             ||||
|||+----------------------------------+----------------------------+|||
||||  16                              |  3                         ||||
|||+----------------------------------+----------------------------+|||
||                         EvaluationResults                         ||
|+--------------------------+-----------------+----------------------+|
||      EvalActionName      |  EvalDecision   |  EvalResourceName    ||
|+--------------------------+-----------------+----------------------+|
||  logs:CreateLogStream    |  allowed        |  *                   ||
|+--------------------------+-----------------+----------------------+|
|||                        MatchedStatements                        |||
||+--------------------------------------+--------------------------+||
|||            SourcePolicyId            |    SourcePolicyType      |||
||+--------------------------------------+--------------------------+||
|||  AmazonSageMakerFullAccess           |  IAM Policy              |||
||+--------------------------------------+--------------------------+||
||||                          EndPosition                          ||||
|||+----------------------------------+----------------------------+|||
||||              Column              |           Line             ||||
|||+----------------------------------+----------------------------+|||
||||  4                               |  284                       ||||
|||+----------------------------------+----------------------------+|||
||||                         StartPosition                         ||||
|||+----------------------------------+----------------------------+|||
||||              Column              |           Line             ||||
|||+----------------------------------+----------------------------+|||
||||  4                               |  177                       ||||
|||+----------------------------------+----------------------------+|||
||                         EvaluationResults                         ||
|+-----------------------+------------------+------------------------+|
||    EvalActionName     |  EvalDecision    |   EvalResourceName     ||
|+-----------------------+------------------+------------------------+|
||  logs:PutLogEvents    |  allowed         |  *                     ||
|+-----------------------+------------------+------------------------+|
|||                        MatchedStatements                        |||
||+--------------------------------------+--------------------------+||
|||            SourcePolicyId            |    SourcePolicyType      |||
||+--------------------------------------+--------------------------+||
|||  AmazonSageMakerFullAccess           |  IAM Policy              |||
||+--------------------------------------+--------------------------+||
||||                          EndPosition                          ||||
|||+----------------------------------+----------------------------+|||
||||              Column              |           Line             ||||
|||+----------------------------------+----------------------------+|||
||||  4                               |  284                       ||||
|||+----------------------------------+----------------------------+|||
||||                         StartPosition                         ||||
|||+----------------------------------+----------------------------+|||
||||              Column              |           Line             ||||
|||+----------------------------------+----------------------------+|||
||||  4                               |  177                       ||||
|||+----------------------------------+----------------------------+|||
----------------------------------------
3️⃣ Verifying inline or attached policies...
--------------------------------------------------------------------------------------
|                              ListAttachedRolePolicies                              |
+------------------------------------------------------------------------------------+
||                                 AttachedPolicies                                 ||
|+----------------------------------------------------+-----------------------------+|
||                      PolicyArn                     |         PolicyName          ||
|+----------------------------------------------------+-----------------------------+|
||  arn:aws:iam::aws:policy/AmazonSageMakerFullAccess |  AmazonSageMakerFullAccess  ||
|+----------------------------------------------------+-----------------------------+|
----------------------------------------
✅ Role validation completed.
If any permissions are missing, attach AmazonSageMakerFullAccess:
aws iam attach-role-policy --role-name AmazonSageMakerExecutionRole --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
✅ All AWS resources created successfully.
python: can't open file '/workspaces/aws-ml-engineering-lifecycle/01_data/scripts/01_generate_data.py': [Errno 2] No such file or directory
2025-07-06 01:12:40,961 [INFO] ✅ Training data saved to: /workspaces/aws-ml-engineering-lifecycle/01_data/processed/sample_realistic_loan_approval_dataset_train.csv
2025-07-06 01:12:40,961 [INFO] ✅ Validation data saved to: /workspaces/aws-ml-engineering-lifecycle/01_data/validation/sample_realistic_loan_approval_dataset_ready_validation.csv
2025-07-06 01:12:41,971 [ERROR] ❌ Transformation failed: [Errno 2] No such file or directory: '01_data/processed/sample_realistic_loan_approval_dataset_train.csv'
🚀 Running all data transformation steps...
🔹 Step 1: Cleaning raw data...
2025-07-06 01:12:42,947 [INFO] 📥 Loaded raw dataset: /workspaces/aws-ml-engineering-lifecycle/01_data/raw/sample_realistic_loan_approval_dataset.csv
2025-07-06 01:12:42,951 [INFO] ✅ Imputed missing 'Age' with median
2025-07-06 01:12:42,952 [INFO] 🧹 Dropped rows with missing LoanApproved: 0 rows removed
2025-07-06 01:12:42,968 [INFO] ✅ Cleaned dataset saved: 01_data/processed/sample_realistic_loan_approval_dataset_cleaned.csv
🔹 Step 2: Encoding categorical features...
2025-07-06 01:12:43,829 [INFO] 📥 Loaded cleaned dataset: 01_data/processed/sample_realistic_loan_approval_dataset_cleaned.csv
2025-07-06 01:12:43,835 [INFO] ✅ One-hot encoded columns: ['Gender', 'EducationLevel']
2025-07-06 01:12:43,861 [INFO] 📤 Encoded dataset saved: 01_data/processed/sample_realistic_loan_approval_dataset_encoded.csv
🔹 Step 3: Fixing booleans and uploading to S3...
2025-07-06 01:12:44,399 [INFO] 📥 Loaded encoded dataset: 01_data/processed/sample_realistic_loan_approval_dataset_encoded.csv
2025-07-06 01:12:44,403 [INFO] ✅ Converted 'LoanApproved' → 'label' [1/0]
2025-07-06 01:12:44,427 [INFO] 📤 Final dataset saved: 01_data/processed/sample_realistic_loan_approval_dataset_ready.csv
2025-07-06 01:12:44,439 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-06 01:12:45,058 [INFO] ✅ Uploaded to S3: s3://btholath-sagemaker-datawrangler-demo/data/sample_realistic_loan_approval_dataset_ready.csv
🔹 Step 4: Validating final dataset...
2025-07-06 01:12:45,507 [INFO] 📄 Dataset loaded for validation.
2025-07-06 01:12:45,508 [INFO] ✅ No missing values found.
2025-07-06 01:12:45,508 [WARNING] ⚠️ Non-numeric columns found: ['CustomerID']
2025-07-06 01:12:45,508 [INFO] ✅ Target column 'label' is binary and valid.
🔹 Step 5: Generating statistics and histograms...
2025-07-06 01:12:46,198 [INFO] 📥 Loaded dataset for EDA: 01_data/processed/sample_realistic_loan_approval_dataset_ready.csv
2025-07-06 01:12:46,199 [INFO] 🧹 Dropped identifier column: CustomerID
2025-07-06 01:12:46,212 [INFO] 📊 Summary statistics saved to: 01_data/eda/summary_statistics.csv
2025-07-06 01:12:46,558 [INFO] 📈 Saved histogram with annotations: 01_data/eda/Age_histogram.png
2025-07-06 01:12:46,952 [INFO] 📈 Saved histogram with annotations: 01_data/eda/Income_histogram.png
2025-07-06 01:12:47,242 [INFO] 📈 Saved histogram with annotations: 01_data/eda/Gender_Male_histogram.png
2025-07-06 01:12:47,684 [INFO] 📈 Saved histogram with annotations: 01_data/eda/Gender_Unspecified_histogram.png
2025-07-06 01:12:47,924 [INFO] 📈 Saved histogram with annotations: 01_data/eda/EducationLevel_Bachelors_Degree_histogram.png
2025-07-06 01:12:48,179 [INFO] 📈 Saved histogram with annotations: 01_data/eda/EducationLevel_High_School_histogram.png
2025-07-06 01:12:48,404 [INFO] 📈 Saved histogram with annotations: 01_data/eda/EducationLevel_Masters_Degree_histogram.png
2025-07-06 01:12:48,701 [INFO] 📈 Saved histogram with annotations: 01_data/eda/EducationLevel_PhD_histogram.png
2025-07-06 01:12:48,948 [INFO] 📈 Saved histogram with annotations: 01_data/eda/label_histogram.png
✅ All data transformation steps completed successfully!
🧠 Running Feature Store setup...
🔹 Step 1: Creating Feature Group...
sagemaker.config INFO - Not applying SDK defaults from location: /etc/xdg/sagemaker/config.yaml
sagemaker.config INFO - Not applying SDK defaults from location: /home/codespace/.config/sagemaker/config.yaml
2025-07-06 01:12:50,807 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-06 01:12:50,896 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-06 01:12:51,042 [INFO] 📥 Loaded dataset: /workspaces/aws-ml-engineering-lifecycle/02_data_preparation/transform/01_data/processed/sample_realistic_loan_approval_dataset_ready.csv
2025-07-06 01:12:51,489 [INFO] ⚠️ Feature Group 'loan-approval-feature-group' already exists. Skipping creation.
⏳ Waiting 30 seconds for Feature Group to initialize...
🔹 Step 2: Ingesting data into Feature Group...
sagemaker.config INFO - Not applying SDK defaults from location: /etc/xdg/sagemaker/config.yaml
sagemaker.config INFO - Not applying SDK defaults from location: /home/codespace/.config/sagemaker/config.yaml
2025-07-06 01:13:23,705 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-06 01:13:23,840 [INFO] 📤 Ingesting 5000 records to Feature Store...
2025-07-06 01:13:24,423 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-06 01:13:24,424 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-06 01:13:24,463 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-06 01:13:24,640 [INFO] Started ingesting index 3334 to 5000
2025-07-06 01:13:24,658 [INFO] Started ingesting index 0 to 1667
2025-07-06 01:13:24,665 [INFO] Started ingesting index 1667 to 3334
2025-07-06 01:15:09,835 [INFO] Successfully ingested row 0 to 1667
2025-07-06 01:15:10,808 [INFO] Successfully ingested row 3334 to 5000
2025-07-06 01:15:10,878 [INFO] Successfully ingested row 1667 to 3334
2025-07-06 01:15:10,902 [INFO] ✅ Ingestion complete.
✅ Feature Store setup and ingestion complete.
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ cd 03_model_training/
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle/03_model_training (main) $ ./run_all_model_training_steps.sh 
🚀 Starting model training pipeline...
🧠 Step 1: Training XGBoost Model
sagemaker.config INFO - Not applying SDK defaults from location: /etc/xdg/sagemaker/config.yaml
sagemaker.config INFO - Not applying SDK defaults from location: /home/codespace/.config/sagemaker/config.yaml
Using SageMaker Role ARN: arn:aws:iam::637423309379:role/AmazonSageMakerExecutionRole
INFO:botocore.credentials:Found credentials in shared credentials file: ~/.aws/credentials
INFO:sagemaker.image_uris:Ignoring unnecessary instance type: None.
INFO:botocore.credentials:Found credentials in shared credentials file: ~/.aws/credentials
INFO:sagemaker.telemetry.telemetry_logging:SageMaker Python SDK will collect telemetry to help us better understand our user's needs, diagnose issues, and deliver additional features.
To opt out of telemetry, please disable via TelemetryOptOut parameter in SDK defaults config. For more information, refer to https://sagemaker.readthedocs.io/en/stable/overview.html#configuring-and-using-defaults-with-the-sagemaker-python-sdk.
INFO:sagemaker:Creating training-job with name: sagemaker-xgboost-2025-07-06-01-16-08-685
2025-07-06 01:16:11 Starting - Starting the training job..

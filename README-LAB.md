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
2025-07-06 01:16:11 Starting - Starting the training job...
2025-07-06 01:16:26 Starting - Preparing the instances for training...
2025-07-06 01:16:46 Downloading - Downloading input data...
2025-07-06 01:17:27 Downloading - Downloading the training image......
2025-07-06 01:18:43 Training - Training image download completed. Training in progress.
2025-07-06 01:18:43 Uploading - Uploading generated training model[2025-07-06 01:18:34.414 ip-10-2-250-52.ec2.internal:6 INFO utils.py:28] RULE_JOB_STOP_SIGNAL_FILENAME: None
[2025-07-06 01:18:34.447 ip-10-2-250-52.ec2.internal:6 INFO profiler_config_parser.py:111] User has disabled profiler.
[2025-07-06:01:18:34:INFO] Imported framework sagemaker_xgboost_container.training
[2025-07-06:01:18:34:INFO] Failed to parse hyperparameter objective value binary:logistic to Json.
Returning the value itself
[2025-07-06:01:18:34:INFO] No GPUs detected (normal if no gpus installed)
[2025-07-06:01:18:34:INFO] Running XGBoost Sagemaker in algorithm mode
[2025-07-06:01:18:34:INFO] Determined 0 GPU(s) available on the instance.
[2025-07-06:01:18:34:INFO] Determined delimiter of CSV input is ','
[2025-07-06:01:18:34:INFO] File path /opt/ml/input/data/train of input files
[2025-07-06:01:18:34:INFO] Making smlinks from folder /opt/ml/input/data/train to folder /tmp/sagemaker_xgboost_input_data
[2025-07-06:01:18:34:INFO] creating symlink between Path /opt/ml/input/data/train/sample_realistic_loan_approval_dataset_ready.csv and destination /tmp/sagemaker_xgboost_input_data/sample_realistic_loan_approval_dataset_ready.csv2119781066709000894
[2025-07-06:01:18:34:INFO] files path: /tmp/sagemaker_xgboost_input_data
[2025-07-06:01:18:34:INFO] Determined delimiter of CSV input is ','
[2025-07-06:01:18:34:INFO] Single node training.
[2025-07-06:01:18:34:INFO] Train matrix has 5001 rows and 9 columns
[2025-07-06 01:18:34.886 ip-10-2-250-52.ec2.internal:6 INFO json_config.py:92] Creating hook from json_config at /opt/ml/input/config/debughookconfig.json.
[2025-07-06 01:18:34.887 ip-10-2-250-52.ec2.internal:6 INFO hook.py:206] tensorboard_dir has not been set for the hook. SMDebug will not be exporting tensorboard summaries.
[2025-07-06 01:18:34.888 ip-10-2-250-52.ec2.internal:6 INFO hook.py:259] Saving to /opt/ml/output/tensors
[2025-07-06 01:18:34.888 ip-10-2-250-52.ec2.internal:6 INFO state_store.py:77] The checkpoint config file /opt/ml/input/config/checkpointconfig.json does not exist.
[2025-07-06:01:18:34:INFO] Debug hook created from config
[2025-07-06 01:18:34.894 ip-10-2-250-52.ec2.internal:6 INFO hook.py:427] Monitoring the collections: metrics
[2025-07-06 01:18:34.897 ip-10-2-250-52.ec2.internal:6 INFO hook.py:491] Hook is writing from the hook with pid: 6
[0]#011train-logloss:0.51314
[1]#011train-logloss:0.39219
[2]#011train-logloss:0.30547
[3]#011train-logloss:0.24091
[4]#011train-logloss:0.19167
[5]#011train-logloss:0.15347
[6]#011train-logloss:0.12347
[7]#011train-logloss:0.09971
[8]#011train-logloss:0.08076
[9]#011train-logloss:0.06556
[10]#011train-logloss:0.05332
[11]#011train-logloss:0.04343
[12]#011train-logloss:0.03542
[13]#011train-logloss:0.02892
[14]#011train-logloss:0.02364
[15]#011train-logloss:0.01934
[16]#011train-logloss:0.01583
[17]#011train-logloss:0.01297
[18]#011train-logloss:0.01064
[19]#011train-logloss:0.00873
[20]#011train-logloss:0.00718
[21]#011train-logloss:0.00590
[22]#011train-logloss:0.00486
[23]#011train-logloss:0.00401
[24]#011train-logloss:0.00331
[25]#011train-logloss:0.00274
[26]#011train-logloss:0.00228
[27]#011train-logloss:0.00189
[28]#011train-logloss:0.00158
[29]#011train-logloss:0.00132
[30]#011train-logloss:0.00111
[31]#011train-logloss:0.00094
[32]#011train-logloss:0.00080
[33]#011train-logloss:0.00068
[34]#011train-logloss:0.00058
[35]#011train-logloss:0.00050
[36]#011train-logloss:0.00043
[37]#011train-logloss:0.00038
[38]#011train-logloss:0.00033
[39]#011train-logloss:0.00029
[40]#011train-logloss:0.00026
[41]#011train-logloss:0.00023
[42]#011train-logloss:0.00021
[43]#011train-logloss:0.00019
[44]#011train-logloss:0.00019
[45]#011train-logloss:0.00019
[46]#011train-logloss:0.00019
[47]#011train-logloss:0.00019
[48]#011train-logloss:0.00019
[49]#011train-logloss:0.00019
[50]#011train-logloss:0.00019
[51]#011train-logloss:0.00019
[52]#011train-logloss:0.00019
[53]#011train-logloss:0.00019
[54]#011train-logloss:0.00019
[55]#011train-logloss:0.00019
[56]#011train-logloss:0.00019
[57]#011train-logloss:0.00019
[58]#011train-logloss:0.00019
[59]#011train-logloss:0.00019
[60]#011train-logloss:0.00019
[61]#011train-logloss:0.00019
[62]#011train-logloss:0.00019
[63]#011train-logloss:0.00019
[64]#011train-logloss:0.00019
[65]#011train-logloss:0.00019
[66]#011train-logloss:0.00019
[67]#011train-logloss:0.00019
[68]#011train-logloss:0.00019
[69]#011train-logloss:0.00019
[70]#011train-logloss:0.00019
[71]#011train-logloss:0.00019
[72]#011train-logloss:0.00019
[73]#011train-logloss:0.00019
[74]#011train-logloss:0.00019
[75]#011train-logloss:0.00019
[76]#011train-logloss:0.00019
[77]#011train-logloss:0.00019
[78]#011train-logloss:0.00019
[79]#011train-logloss:0.00019
[80]#011train-logloss:0.00019
[81]#011train-logloss:0.00019
[82]#011train-logloss:0.00019
[83]#011train-logloss:0.00019
[84]#011train-logloss:0.00019
[85]#011train-logloss:0.00019
[86]#011train-logloss:0.00019
[87]#011train-logloss:0.00019
[88]#011train-logloss:0.00019
[89]#011train-logloss:0.00019
[90]#011train-logloss:0.00019
[91]#011train-logloss:0.00019
[92]#011train-logloss:0.00019
[93]#011train-logloss:0.00019
[94]#011train-logloss:0.00019
[95]#011train-logloss:0.00019
[96]#011train-logloss:0.00019
[97]#011train-logloss:0.00019
[98]#011train-logloss:0.00019
[99]#011train-logloss:0.00019

2025-07-06 01:18:56 Completed - Training job completed
Training seconds: 130
Billable seconds: 130
INFO:__main__:✅ XGBoost training job submitted
🔍 Step 2: Monitoring Training Job
INFO:botocore.credentials:Found credentials in shared credentials file: ~/.aws/credentials
INFO:root:📊 Training job 'sagemaker-xgboost-2025-07-06-01-16-08-685' status: Completed
INFO:root:📦 Model saved to: s3://btholath-sagemaker-datawrangler-demo/output/sagemaker-xgboost-2025-07-06-01-16-08-685/output/model.tar.gz
📈 Step 3: Running Hyperparameter Optimization (HPO)
sagemaker.config INFO - Not applying SDK defaults from location: /etc/xdg/sagemaker/config.yaml
sagemaker.config INFO - Not applying SDK defaults from location: /home/codespace/.config/sagemaker/config.yaml
INFO:sagemaker.image_uris:Ignoring unnecessary instance type: None.
INFO:botocore.credentials:Found credentials in shared credentials file: ~/.aws/credentials
INFO:botocore.credentials:Found credentials in shared credentials file: ~/.aws/credentials
WARNING:sagemaker.estimator:No finished training job found associated with this estimator. Please make sure this estimator is only used for building workflow config
INFO:sagemaker:Creating hyperparameter tuning job with name: xgb-hpo-250706-0119
╭─────────────────────────────── Traceback (most recent call last) ────────────────────────────────╮
│ /workspaces/aws-ml-engineering-lifecycle/03_model_training/hpo/01_run_hpo_job.py:127 in <module> │
│                                                                                                  │
│   124                                                                                            │
│   125                                                                                            │
│   126 if __name__ == "__main__":                                                                 │
│ ❱ 127 │   main()                                                                                 │
│   128                                                                                            │
│                                                                                                  │
│ /workspaces/aws-ml-engineering-lifecycle/03_model_training/hpo/01_run_hpo_job.py:122 in main     │
│                                                                                                  │
│   119 │   │   content_type="csv"                                                                 │
│   120 │   )                                                                                      │
│   121 │                                                                                          │
│ ❱ 122 │   tuner.fit({"train": train_input, "validation": validation_input})                      │
│   123 │   logger.info(f"🚀 HPO job submitted: {tuning_job_name}")                                │
│   124                                                                                            │
│   125                                                                                            │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/sagemaker/workflow/pipeline_context.py:346 │
│ in wrapper                                                                                       │
│                                                                                                  │
│   343 │   │   │                                                                                  │
│   344 │   │   │   return _StepArguments(retrieve_caller_name(self_instance), run_func, *args,    │
│   345 │   │                                                                                      │
│ ❱ 346 │   │   return run_func(*args, **kwargs)                                                   │
│   347 │                                                                                          │
│   348 │   return wrapper                                                                         │
│   349                                                                                            │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/sagemaker/tuner.py:1034 in fit             │
│                                                                                                  │
│   1031 │   │   │   │   arguments are needed.                                                     │
│   1032 │   │   """                                                                               │
│   1033 │   │   if self.estimator is not None:                                                    │
│ ❱ 1034 │   │   │   self._fit_with_estimator(inputs, job_name, include_cls_metadata, **kwargs)    │
│   1035 │   │   else:                                                                             │
│   1036 │   │   │   self._fit_with_estimator_dict(inputs, job_name, include_cls_metadata, estima  │
│   1037                                                                                           │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/sagemaker/tuner.py:1045 in                 │
│ _fit_with_estimator                                                                              │
│                                                                                                  │
│   1042 │   │   """Start tuning for tuner instances that have the ``estimator`` field set."""     │
│   1043 │   │   self._prepare_estimator_for_tuning(self.estimator, inputs, job_name, **kwargs)    │
│   1044 │   │   self._prepare_for_tuning(job_name=job_name, include_cls_metadata=include_cls_met  │
│ ❱ 1045 │   │   self.latest_tuning_job = _TuningJob.start_new(self, inputs)                       │
│   1046 │                                                                                         │
│   1047 │   def _fit_with_estimator_dict(self, inputs, job_name, include_cls_metadata, estimator  │
│   1048 │   │   """Start tuning for tuner instances that have the ``estimator_dict`` field set."  │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/sagemaker/tuner.py:2143 in start_new       │
│                                                                                                  │
│   2140 │   │   """                                                                               │
│   2141 │   │   tuner_args = cls._get_tuner_args(tuner, inputs)                                   │
│   2142 │   │                                                                                     │
│ ❱ 2143 │   │   tuner.sagemaker_session.create_tuning_job(**tuner_args)                           │
│   2144 │   │                                                                                     │
│   2145 │   │   return cls(tuner.sagemaker_session, tuner._current_job_name)                      │
│   2146                                                                                           │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/sagemaker/session.py:3398 in               │
│ create_tuning_job                                                                                │
│                                                                                                  │
│   3395 │   │   │   logger.debug("tune request: %s", json.dumps(request, indent=4))               │
│   3396 │   │   │   self.sagemaker_client.create_hyper_parameter_tuning_job(**request)            │
│   3397 │   │                                                                                     │
│ ❱ 3398 │   │   self._intercept_create_request(tune_request, submit, self.create_tuning_job.__na  │
│   3399 │                                                                                         │
│   3400 │   def _get_tuning_request(                                                              │
│   3401 │   │   self,                                                                             │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/sagemaker/session.py:6819 in               │
│ _intercept_create_request                                                                        │
│                                                                                                  │
│   6816 │   │   │   create (functor): a functor calls the sagemaker client create method          │
│   6817 │   │   │   func_name (str): the name of the function needed intercepting                 │
│   6818 │   │   """                                                                               │
│ ❱ 6819 │   │   return create(request)                                                            │
│   6820 │                                                                                         │
│   6821 │   def _create_inference_recommendations_job_request(                                    │
│   6822 │   │   self,                                                                             │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/sagemaker/session.py:3396 in submit        │
│                                                                                                  │
│   3393 │   │   def submit(request):                                                              │
│   3394 │   │   │   logger.info("Creating hyperparameter tuning job with name: %s", job_name)     │
│   3395 │   │   │   logger.debug("tune request: %s", json.dumps(request, indent=4))               │
│ ❱ 3396 │   │   │   self.sagemaker_client.create_hyper_parameter_tuning_job(**request)            │
│   3397 │   │                                                                                     │
│   3398 │   │   self._intercept_create_request(tune_request, submit, self.create_tuning_job.__na  │
│   3399                                                                                           │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/botocore/client.py:601 in _api_call        │
│                                                                                                  │
│    598 │   │   │   │   │   f"{py_operation_name}() only accepts keyword arguments."              │
│    599 │   │   │   │   )                                                                         │
│    600 │   │   │   # The "self" in this scope is referring to the BaseClient.                    │
│ ❱  601 │   │   │   return self._make_api_call(operation_name, kwargs)                            │
│    602 │   │                                                                                     │
│    603 │   │   _api_call.__name__ = str(py_operation_name)                                       │
│    604                                                                                           │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/botocore/context.py:123 in wrapper         │
│                                                                                                  │
│   120 │   │   │   with start_as_current_context():                                               │
│   121 │   │   │   │   if hook:                                                                   │
│   122 │   │   │   │   │   hook()                                                                 │
│ ❱ 123 │   │   │   │   return func(*args, **kwargs)                                               │
│   124 │   │                                                                                      │
│   125 │   │   return wrapper                                                                     │
│   126                                                                                            │
│                                                                                                  │
│ /usr/local/python/3.12.1/lib/python3.12/site-packages/botocore/client.py:1074 in _make_api_call  │
│                                                                                                  │
│   1071 │   │   │   │   "Code"                                                                    │
│   1072 │   │   │   )                                                                             │
│   1073 │   │   │   error_class = self.exceptions.from_code(error_code)                           │
│ ❱ 1074 │   │   │   raise error_class(parsed_response, operation_name)                            │
│   1075 │   │   else:                                                                             │
│   1076 │   │   │   return parsed_response                                                        │
│   1077                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
ClientError: An error occurred (ValidationException) when calling the CreateHyperParameterTuningJob operation: No S3 objects found under S3 URL 
"s3://btholath-sagemaker-datawrangler-demo/data/validation/sample_realistic_loan_approval_dataset_ready.csv" given in input data source. Please ensure that the bucket 
exists in the selected region (us-east-1), that objects exist under that S3 prefix, and that the role "arn:aws:iam::637423309379:role/AmazonSageMakerExecutionRole" has
"s3:ListBucket" permissions on bucket "btholath-sagemaker-datawrangler-demo".
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle/03_model_training (main) $ 
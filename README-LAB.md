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

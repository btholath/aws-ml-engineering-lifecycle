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
- /workspaces/aws-ml-engineering-lifecycle/02_model_training/train_xgboost_loan_predictor.py

```bash
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ python 02_model_training/train_xgboost_loan_predictor.py
sagemaker.config INFO - Not applying SDK defaults from location: /etc/xdg/sagemaker/config.yaml
sagemaker.config INFO - Not applying SDK defaults from location: /home/codespace/.config/sagemaker/config.yaml
2025-07-04 22:54:31,807 [INFO] Found credentials in shared credentials file: ~/.aws/credentials
2025-07-04 22:54:31,914 [INFO] Ignoring unnecessary instance type: None.
2025-07-04 22:54:31,914 [INFO] Using XGBoost image URI: 683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1
2025-07-04 22:54:31,914 [INFO] Starting SageMaker training job...
2025-07-04 22:54:32,557 [INFO] ✅ Training job created: real-loan-predictor-xgb-1751669671
2025-07-04 22:54:32,557 [INFO] 📦 Output S3 path: s3://btholath-sagemaker-datawrangler-demo/real-loan-predictor-output/
2025-07-04 22:54:32,557 [INFO] 🔗 Job ARN: arn:aws:sagemaker:us-east-1:637423309379:training-job/real-loan-predictor-xgb-1751669671
@btholath ➜ /workspaces/aws-ml-engineering-lifecycle (main) $ 

You should be seeing the training job in aws console at https://us-east-1.console.aws.amazon.com/sagemaker/home?region=us-east-1#/jobs
```


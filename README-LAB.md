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
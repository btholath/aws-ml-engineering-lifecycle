cd 00_infrastructure
./create_all_resources.sh     # Sets up IAM role, security group, S3, and Studio domain

cd ../01_data
python scripts/01_generate_data.py
python scripts/02_split_validation_data.py
python scripts/03_transform_data.py

cd ../02_data_preparation/transform
./run_all_transform_steps.sh  # Run 01 to 05 steps

cd ../feature_store
./run_all_feature_store_steps.sh

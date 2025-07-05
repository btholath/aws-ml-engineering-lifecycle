#!/bin/bash
# run_data_wrangler_flow.sh

echo "⚙️ Generating flow file..."
python 02_data_preparation/data_wrangler/01_generate_flow.py

echo "☁️ Uploading to S3..."
python 02_data_preparation/data_wrangler/02_upload_flow.py

echo "✅ Done. Import the flow in SageMaker Studio → Data Wrangler."

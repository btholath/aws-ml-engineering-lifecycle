# File: 01_data_preparation/data_wrangler/patch_flow_template.py

import os
import json
import logging
from dotenv import load_dotenv

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Inputs
template_path = "01_data_preparation/data_wrangler/template.flow"
output_path = "01_data_preparation/data_wrangler/customer_sales_cleaning.flow"
s3_uri = os.getenv("S3_URI")

if not s3_uri:
    logging.error("Missing S3_URI in .env file")
    exit(1)

try:
    with open(template_path, "r") as f:
        flow = json.load(f)

    # Patch S3 URI and flow name
    flow["source"]["parameters"]["s3Uri"] = s3_uri
    flow["metadata"]["flowName"] = "customer_sales_cleaning"

    # Save new flow
    with open(output_path, "w") as f:
        json.dump(flow, f, indent=4)

    logging.info(f"✅ Patched .flow file saved: {output_path}")

except Exception as e:
    logging.error(f"❌ Failed to patch flow file: {e}")
    exit(1)

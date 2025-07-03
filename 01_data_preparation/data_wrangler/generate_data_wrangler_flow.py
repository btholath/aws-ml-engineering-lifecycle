# File: 01_data_preparation/data_wrangler/generate_data_wrangler_flow.py

import os
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Environment configs
S3_URI = os.getenv("S3_URI")
FLOW_NAME = os.getenv("FLOW_NAME", "data_wrangler_flow")
FLOW_OUTPUT_DIR = os.getenv("FLOW_OUTPUT_DIR", "01_data_preparation/data_wrangler")

if not S3_URI:
    logging.error("Missing S3_URI in .env file")
    exit(1)

# Ensure output directory exists
os.makedirs(FLOW_OUTPUT_DIR, exist_ok=True)
flow_file_path = os.path.join(FLOW_OUTPUT_DIR, f"{FLOW_NAME}.flow")

# Define the Data Wrangler Flow JSON
flow = {
    "nodes": [
        {
            "node_id": "source_1",
            "node_type": "SOURCE",
            "parameters": {
                "source": "S3",
                "s3_uri": S3_URI,
                "format": "CSV",
                "delimiter": ",",
                "compression": "NONE",
                "header": "true"
            }
        },
        {
            "node_id": "fill_missing_age",
            "node_type": "TRANSFORM",
            "upstream_nodes": ["source_1"],
            "parameters": {
                "transform_type": "IMPUTE",
                "impute_column": "Age",
                "impute_strategy": "MEDIAN"
            }
        },
        {
            "node_id": "encode_gender_country",
            "node_type": "TRANSFORM",
            "upstream_nodes": ["fill_missing_age"],
            "parameters": {
                "transform_type": "ENCODE",
                "columns_to_encode": ["Gender", "Country"],
                "encoding_strategy": "ONE_HOT"
            }
        },
        {
            "node_id": "rename_column",
            "node_type": "TRANSFORM",
            "upstream_nodes": ["encode_gender_country"],
            "parameters": {
                "transform_type": "RENAME",
                "rename_map": {
                    "PurchaseAmount": "Purchase_Value"
                }
            }
        }
    ],
    "metadata": {
        "flow_name": FLOW_NAME,
        "version": "1.0",
        "created_by": "automated-script",
        "description": "Flow for cleaning and transforming customer sales dataset"
    }
}

# Write the .flow file
try:
    with open(flow_file_path, "w") as f:
        json.dump(flow, f, indent=4)
    logging.info(f"✅ Data Wrangler flow file saved: {flow_file_path}")
except Exception as e:
    logging.error(f"❌ Failed to save flow file: {e}")
    exit(1)

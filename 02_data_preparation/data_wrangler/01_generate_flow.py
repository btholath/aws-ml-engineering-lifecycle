"""
generates a .flow file used by SageMaker Data Wrangler GUI.

✅ Tasks Performed:
Define data source (e.g., S3 CSV)

Specify transformations (impute, encode, rename, etc.)

Save a .flow file in your project
"""

# 01_generate_flow.py

import os
import json
import logging
from dotenv import load_dotenv

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

S3_URI = os.getenv("S3_URI")
FLOW_NAME = os.getenv("FLOW_NAME", "data_wrangler_flow")
FLOW_OUTPUT_DIR = "02_data_preparation/data_wrangler"
flow_file_path = os.path.join(FLOW_OUTPUT_DIR, f"{FLOW_NAME}.flow")

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
        "description": "Flow for cleaning and transforming sales dataset"
    }
}

# Save flow
os.makedirs(FLOW_OUTPUT_DIR, exist_ok=True)
with open(flow_file_path, "w") as f:
    json.dump(flow, f, indent=4)

logging.info(f"✅ Flow file saved: {flow_file_path}")

#!/bin/bash
set -e

echo "🗑️ Cleaning up SageMaker Studio and S3 bucket..."
./04_cleanup_resources.sh

echo "⚠️ Cleaning up SageMaker model packages, roles, endpoints..."
./05_check_resource_status.sh

echo "✅ All AWS resources deleted."

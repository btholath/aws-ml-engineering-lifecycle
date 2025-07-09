<pre>
1. model_packaging/
   ├── 01_create_model_artifact.py          # Prepares model file from training
   ├── 02_prepare_container_image.py        # (Optional) Prepares Docker image if custom

2. real_time/
   ├── 01_deploy_endpoint.py                # Deploys model to real-time endpoint
   ├── 02_invoke_endpoint.py                # Invokes the deployed endpoint
   ├── 03_config_autoscaling.py             # (Optional) Configures autoscaling
   ├── 04_teardown_endpoint.py              # Deletes endpoint after use

3. batch/
   ├── 01_batch_transform.py                # Starts batch transform job
   ├── 02_fetch_results.py                  # Fetches and saves results

</pre>

Testing Individual Steps (optional)
```bash
python model_packaging/01_create_model_artifact.py
python real_time/01_deploy_endpoint.py
python batch/01_batch_transform.py
```

Teardown (cleanup real-time endpoint)
```bash
python real_time/04_teardown_endpoint.py
```
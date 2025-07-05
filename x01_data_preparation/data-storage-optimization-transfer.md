
***Data Storage and Transfer Optimization***
-   Efficient storage and transfer reduce costs and improve performance
-   Vital for large-scale machine learning workflows
-   Minimizes latency, optimized data paths
    -   Speed up training and inference
-   Scales with demand
-   Ensures data intrgrity and security during transfers    


***Strategies for Data Transfer***
-   Use AWS DataSync for bulk transfers
-   Enable S3 Transfer Acceleration for faster uploads
-   Leverage Amazon FSx for Lustre
    -  High-performace file systems
    -  Optimized for workloads requiring low latency and high throughput
    -  Great for many small files


***Optimizing Large Dataset Training***
-   Use pipe mode to train a model on terabytes of medical imaging data.
-   Partition data into smaller shards to distribute across multiple training instances
-   Monitor data transfer rates using CloudWatch to identify and resolve bottlenecks.
-   Utilize SageMaker's managed spot training to dynamically allocate Spot Instances.
    -   Adds cost-efficiency and automatic retries via checkpoints.
    -   Can tolerate interruption


***Data Transformation***
-   SageMaker Data Wrangler
    -   Workflows
        -   Data selection
        -   Tranformation
        -   Storage
    -   Support for:
        -   Missing values
        -   Normalization
        -   Transformations    
-   AWS Glue
    -   Transform and move into S3
    -   Compatible with SageMaker        
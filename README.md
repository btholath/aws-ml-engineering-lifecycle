# aws-ml-engineering-lifecycle
End-to-end AWS Machine Learning engineering toolkit to build, deploy, and maintain ML solutions. Covers data prep, modeling, CI/CD pipelines, model monitoring, security, and infrastructure automation—aligned with AWS ML Engineer certification objectives.


**Domain 4: ML Solution Monitoring, Maintenance, and Security**
----------
**Task Statement 4.1: Monitor model inference.**
**Knowledge of:**
-   Drift in ML models
-   Techniques to monitor data quality and model performance
-   Design principles for ML lenses relevant to monitoring


**Skills in:**
-   Monitoring models in production (for example, by using SageMaker Model Monitor)
-   Monitoring workflows to detect anomalies or errors in data processing or model inference
-   Detecting changes in the distribution of data that can affect model performance (for example, by using SageMaker Clarify)
-   Monitoring model performance in production by using A/B testing

----------

**Task Statement 4.2: Monitor and optimize infrastructure and costs.**
**Knowledge of:**
-   Key performance metrics for ML infrastructure (for example, utilization, throughput, availability, scalability, fault tolerance)
-   Monitoring and observability tools to troubleshoot latency and performance issues (for example, AWS X-Ray, Amazon CloudWatch Lambda Insights, Amazon CloudWatch Logs Insights)
-   How to use AWS CloudTrail to log, monitor, and invoke re-training activities 
-   Differences between instance types and how they affect performance (for
example, memory optimized, compute optimized, general purpose, inference optimized)
-   Capabilities of cost analysis tools (for example, AWS Cost Explorer, AWS Billing and Cost Management, AWS Trusted Advisor)
-   Cost tracking and allocation techniques (for example, resource tagging)

**Skills in:**
-   Configuring and using tools to troubleshoot and analyze resources (for example, CloudWatch Logs, CloudWatch alarms)
-   Creating CloudTrail trails
-   Setting up dashboards to monitor performance metrics (for example, by using Amazon QuickSight, CloudWatch dashboards)
-   Monitoring infrastructure (for example, by using EventBridge events)
-   Rightsizing instance families and sizes (for example, by using SageMaker Inference Recommender and AWS Compute Optimizer)
-   Monitoring and resolving latency and scaling issues
-   Preparing infrastructure for cost monitoring (for example, by applying a tagging strategy)
-   Troubleshooting capacity concerns that involve cost and performance (for example, provisioned concurrency, service quotas, auto scaling)
-   Optimizing costs and setting cost quotas by using appropriate cost management tools (for example, AWS Cost Explorer, AWS Trusted Advisor, AWS Budgets)
-   Optimizing infrastructure costs by selecting purchasing options (for example, Spot Instances, On-Demand Instances, Reserved Instances, SageMaker Savings Plans)

----------

**Task Statement 4.3: Secure AWS resources.**

**Knowledge of:**
-   IAM roles, policies, and groups that control access to AWS services (for example, AWS Identity and Access Management [IAM], bucket policies, SageMaker Role Manager)
-   SageMaker security and compliance features
-   Controls for network access to ML resources
-   Security best practices for CI/CD pipelines

**Skills in:**
-   Configuring least privilege access to ML artifacts
-   Configuring IAM policies and roles for users and applications that interact with ML systems
-   Monitoring, auditing, and logging ML systems to ensure continued security and compliance
-   Troubleshooting and debugging security issues
-   Building VPCs, subnets, and security groups to securely isolate ML systems



***build_ml_environment.sh - Follow the full end-to-end ML pipeline sequence:***
-   Provision infrastructure.
-   Prepare and clean data.
-   Run transformation, feature store setup, and EDA.
-   Train model and run HPO.
-   Register and deploy model.
-   Run batch inference and evaluate.

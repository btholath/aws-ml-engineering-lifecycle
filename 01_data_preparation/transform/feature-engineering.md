***What is Feature Engineering***
-   Transforms raw data into meaningful input features
-   Improves performance of ML models
-   Preprocesses and transforms
    -   One-Hot Encoding
    -   Label Encoding
    -   Min-Max Scaling
    -   Standardization (Z-score)
    -   Log Transformation
    -   Clipping
    -   Missing Value Imputation
    -   Outlier Detection


***Importance of Data Cleaning***
-   Ensure data quality for accurate ML model training
-   Reduces noise, errors, and inconsitencies
-   Prevents issues like overfitting or poor model generalization.
-   Data Wrangler has options for handling missing data.


***Data Quality Analysis***
-   Summary staticstics
    -   Mean
    -   Median
    -   Standard deviation
-   Correlation matrices
-   Distribution histograms
- Identify inconsitencies or biases in data


***Exporting Processed Data***
Export processed data to:
    -   Amazon S3 for storage
    -   Direct input for SageMaker training jobs
    -   Redshift or other databases for further analysis

***Integration with SageMaker Pipelines***
-   Data Wrangler integrates seamlessly with SageMaker Pipelines
-   Allows preprocessing workflows to become part of CI/CD pipelines.
-   Ensures consistency in training and production environments.


***Feature***
-   An individual measurable property or characteric of the data that is used as input to a machne learning model.
-   Types:
    -   Numerical - e.g., age
    -   Categorical - e.g., color
    -   Textual -e.g., words
    -   Derived Features    - e.g., ratios
    
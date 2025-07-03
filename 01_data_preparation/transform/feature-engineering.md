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

***Feature Scaling***
-   Ensures all features contribute equally to model training.
-   Prevents features with larger scales from dominating
-   Speeds up convergence of gradient descent algorithms
-   Reduces risk of numerical instability in computations
-   Normalization vs. Standadization
    -   Normalization
        -   Scales values to a [0,1] range; suitable for bounded features.
    -   Standarization
        -   Transforms data to have a mean of 0 and a standard deviation of 1.
    - Helps in models like k-NN and SVMs where distance-based measures are used.
    - Normalization is sensitive to outliers; standarization is more robust.
-   Use Cases
    - Improved performance in models like logistic regression and neral networks.
    - Faster convergence in gradient-based optimizatoion methods
    - Harmonizing feature contributions.
    - Example: Scaling features for an XGBoost fradu detection model.


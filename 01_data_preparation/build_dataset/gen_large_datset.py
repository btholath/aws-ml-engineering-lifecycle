#!/usr/bin/python3 
import numpy as np
import pandas as pd

# Set seed for reproducibility
np.random.seed(42)

# Generate a large dataset with complex interactions
num_samples = 1_000_000  # 1 million rows
num_features = 10  # 10 features

# Create features with non-linear relationships
X = np.random.rand(num_samples, num_features) * 100  # Scale to a range [0, 100]

# Generate a target variable with a complex function
y = (
    5 * np.sin(X[:, 0]) +
    3 * np.log(X[:, 1] + 1) +
    2 * np.sqrt(X[:, 2]) +
    X[:, 3] ** 1.5 -
    4 * X[:, 4] ** 2 +
    np.tan(X[:, 5] / 10) +
    np.exp(-X[:, 6] / 50) +
    np.random.normal(scale=10, size=num_samples)  # Add some noise
)

# Create a DataFrame
columns = [f"Feature_{i}" for i in range(num_features)]
df = pd.DataFrame(X, columns=columns)
df["Target"] = y


# Save to CSV
df.to_csv("./dataset/sample_large_dataset_10M.csv", index=False)


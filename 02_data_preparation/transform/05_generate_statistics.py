"""
Script: 05_generate_statistics.py
Purpose: Generate basic statistics and annotated histograms for EDA.
"""

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load .env and configure logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Paths
input_csv = "01_data/processed/sample_realistic_loan_approval_dataset_ready.csv"
output_dir = "01_data/eda"
os.makedirs(output_dir, exist_ok=True)

try:
    df = pd.read_csv(input_csv)
    logging.info(f"📥 Loaded dataset for EDA: {input_csv}")

    # Drop ID column
    if "CustomerID" in df.columns:
        df = df.drop(columns=["CustomerID"])
        logging.info("🧹 Dropped identifier column: CustomerID")

    # Save summary statistics
    stats_csv = os.path.join(output_dir, "summary_statistics.csv")
    df.describe().to_csv(stats_csv)
    logging.info(f"📊 Summary statistics saved to: {stats_csv}")

    # Generate annotated histograms
    for col in df.select_dtypes(include="number").columns:
        plt.figure(figsize=(8, 5))
        ax = df[col].hist(bins=30, color='skyblue', edgecolor='black', grid=True)
        mean_val = df[col].mean()
        median_val = df[col].median()

        # Annotate mean/median
        plt.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f"Mean: {mean_val:.2f}")
        plt.axvline(median_val, color='green', linestyle='--', linewidth=1.5, label=f"Median: {median_val:.2f}")

        # Annotated description
        plt.title(f"Distribution of '{col}'")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.legend(loc="upper right")
        plt.text(
            0.95, 0.02,
            "This chart shows how values are spread out.\nRed = mean, Green = median.",
            transform=plt.gca().transAxes,
            fontsize=8,
            color='gray',
            verticalalignment='bottom',
            horizontalalignment='right'
        )

        # Save
        fig_path = os.path.join(output_dir, f"{col}_histogram.png")
        plt.tight_layout()
        plt.savefig(fig_path)
        plt.close()
        logging.info(f"📈 Saved histogram with annotations: {fig_path}")

except Exception as e:
    logging.error(f"❌ Failed to generate statistics: {e}")
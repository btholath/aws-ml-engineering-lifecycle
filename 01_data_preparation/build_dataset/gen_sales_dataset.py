#!/usr/bin/python3


import pandas as pd
import random

# Define sample data
customer_ids = [f"CUST{str(i).zfill(5)}" for i in range(1, 5001)]
ages = [random.randint(18, 80) for _ in range(5000)]
genders = [random.choice(["Male", "Female", "Unspecified"]) for _ in range(5000)]
products = [random.choice(["Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch", "Camera", "Monitor", "Keyboard", "Mouse", "Speaker"]) for _ in range(5000)]
purchase_amounts = [round(random.uniform(20, 3000), 2) for _ in range(5000)]
countries = [random.choice(["USA", "Canada", "UK", "Germany", "France", "Australia", "Japan", "India", "Brazil", "South Africa"]) for _ in range(5000)]

# Create DataFrame
df = pd.DataFrame({
    "CustomerID": customer_ids,
    "Age": ages,
    "Gender": genders,
    "Product": products,
    "PurchaseAmount": purchase_amounts,
    "Country": countries
})

# Save to CSV
df.to_csv("./dataset/sample_sales_dataset.csv", index=False)


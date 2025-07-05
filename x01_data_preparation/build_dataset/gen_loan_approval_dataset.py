#!/usr/bin/python3

import pandas as pd
import random

# Define sample data
education_levels = ["High School", "Associate Degree", "Bachelor's Degree", "Master's Degree", "PhD"]
genders = ["Male", "Female", "Unspecified"]

# Generate data
customer_ids = [f"CUST{str(i).zfill(5)}" for i in range(1, 5001)]
ages = [random.randint(18, 80) for _ in range(5000)]
genders = [random.choice(genders) for _ in range(5000)]
education_levels = [random.choice(education_levels) for _ in range(5000)]
incomes = [round(random.uniform(20000, 150000), 2) for _ in range(5000)]
loan_approved = [random.choice([True, False]) for _ in range(5000)]

# Create DataFrame
df = pd.DataFrame({
    "CustomerID": customer_ids,
    "Age": ages,
    "Gender": genders,
    "EducationLevel": education_levels,
    "Income": incomes,
    "LoanApproved": loan_approved
})



# Save to CSV
df.to_csv("./dataset/sample_loan_approval_dataset.csv", index=False)


#!/usr/bin/python3

import pandas as pd
import random

# Define sample data categories
education_levels = ["High School", "Associate Degree", "Bachelor's Degree", "Master's Degree", "PhD"]
genders = ["Male", "Female", "Unspecified"]

# Function to generate loan approval probability based on features
def approve_loan(age, income, education_level):
    """
    Simulates loan approval probability based on basic factors:
    - Higher education and income increase approval chances.
    - Older customers with stable income are more likely to be approved.
    """
    base_prob = 0.2  # Base approval probability

    # Increase probability based on income
    if income > 100000:
        base_prob += 0.4
    elif income > 75000:
        base_prob += 0.3
    elif income > 50000:
        base_prob += 0.2

    # Education factor
    if education_level == "PhD":
        base_prob += 0.2
    elif education_level == "Master's Degree":
        base_prob += 0.15
    elif education_level == "Bachelor's Degree":
        base_prob += 0.1
    elif education_level == "Associate Degree":
        base_prob += 0.05

    # Age factor (older customers with stable income are more reliable)
    if 30 <= age <= 60:
        base_prob += 0.1

    # Ensure probability is between 0 and 1
    base_prob = min(max(base_prob, 0), 1)

    return random.random() < base_prob  # Return True if approved, False otherwise

# Generate dataset
customer_ids = [f"CUST{str(i).zfill(5)}" for i in range(1, 5001)]
ages = [random.randint(18, 80) for _ in range(5000)]
genders = [random.choice(genders) for _ in range(5000)]
education_levels = [random.choice(education_levels) for _ in range(5000)]
incomes = [round(random.uniform(20000, 150000), 2) for _ in range(5000)]
loan_approved = [approve_loan(ages[i], incomes[i], education_levels[i]) for i in range(5000)]

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
df.to_csv("./dataset/sample_realistic_loan_approval_dataset.csv", index=False)


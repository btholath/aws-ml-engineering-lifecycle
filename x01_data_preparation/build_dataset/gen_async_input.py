#!/usr/bin/python3

import pandas as pd
import random

# Generate data
ages = [random.randint(18, 80) for _ in range(5000)]
education_levels = [random.randint(0,4) for _ in range(5000)]
incomes = [round(random.uniform(20000, 150000), 0) for _ in range(5000)]

# Create DataFrame
df = pd.DataFrame({
    "Age": ages,
    "EducationLevel": education_levels,
    "Income": incomes,
})



# Save to CSV
df.to_csv("./dataset/async-input.csv", index=False)


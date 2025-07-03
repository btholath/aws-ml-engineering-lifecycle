#!/usr/bin/python3

import uuid
import random
import csv
from datetime import datetime, timedelta

# Define ranges for home attributes
NUM_RECORDS = 50000
PRICE_BASE = 100000  # Base price
PRICE_BEDROOM_MODIFIER = 15000
PRICE_BATHROOM_MODIFIER = 10000
PRICE_DISTANCE_MODIFIER = 5000

# Generate dataset
records = []
for _ in range(NUM_RECORDS):
    sale_id = str(uuid.uuid4())
    sale_timestamp = (datetime.now() - timedelta(days=random.randint(0, 365 * 5))).strftime('%Y-%m-%dT%H:%M:%SZ')
    home_built_date = datetime.now().year - random.randint(10, 80)  # Homes built within last 80 years
    bedrooms = random.randint(1, 6)
    bathrooms = random.randint(1, 4)
    distance_to_school = round(random.uniform(0.1, 10.0), 2)  # Distance in miles
    
    # Price adjustments
    price = PRICE_BASE + (bedrooms * PRICE_BEDROOM_MODIFIER) + (bathrooms * PRICE_BATHROOM_MODIFIER)
    price *= 1.1 if distance_to_school < 1 else 1.0  # Higher price if closer to school
    price = round(price + (random.uniform(-5000, 5000)), 2)  # Add slight randomness
    
    records.append([
        sale_id, sale_timestamp, home_built_date, price, distance_to_school, bedrooms, bathrooms
    ])

# Write to CSV
csv_filename = "./dataset/sample_home_sales_dataset.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "timestamp", "built", "price", "distanceToElem", "bedrooms", "bathrooms"])
    writer.writerows(records)

print(f"Dataset generated and saved as {csv_filename}")


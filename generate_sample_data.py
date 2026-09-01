"""
Generates a messy synthetic retail transaction dataset to demonstrate the
cleaning pipeline: duplicate rows, missing values, inconsistent casing,
and stray whitespace, the same kinds of issues real merchant/transaction
data actually has.
"""

import random
import csv

random.seed(42)

customers = [f"C{1000+i}" for i in range(60)]
products = [
    "Bluetooth Headphones", "Phone Case", "USB-C Cable", "Laptop Stand",
    "Wireless Mouse", "Mechanical Keyboard", "Webcam", "Desk Lamp",
    "Screen Protector", "Portable Charger", "HDMI Adapter", "Laptop Sleeve",
]

rows = []
for _ in range(650):
    cust = random.choice(customers)
    n_items = random.randint(1, 4)
    basket = random.sample(products, n_items)
    order_id = f"O{random.randint(10000, 99999)}"
    for prod in basket:
        price = round(random.uniform(8, 180), 2)
        qty = random.randint(1, 3)

        # inject messiness
        cust_id = cust
        if random.random() < 0.05:
            cust_id = cust.lower()  # inconsistent casing
        prod_name = prod
        if random.random() < 0.08:
            prod_name = f"  {prod}  "  # stray whitespace
        if random.random() < 0.05:
            prod_name = prod.upper()

        price_val = price
        if random.random() < 0.04:
            price_val = ""  # missing price

        rows.append([order_id, cust_id, prod_name, qty, price_val])

# inject exact duplicate rows
for _ in range(25):
    rows.append(random.choice(rows).copy())

random.shuffle(rows)

with open("sample_transactions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["order_id", "customer_id", "product", "quantity", "unit_price"])
    writer.writerows(rows)

print(f"Generated {len(rows)} rows to sample_transactions.csv")

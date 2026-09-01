# Customer Data Cleaning & Insights Pipeline

A Python pipeline that takes messy retail transaction data, duplicate
rows, missing prices, inconsistent casing and whitespace, and turns it
into a cleaned dataset, customer segments, and a market-basket analysis
of which products get bought together.

## Why I built this

This project generalizes the kind of work I did as a Data Science Intern
at Business Intelligence Analytics Inc., cleaning and organizing master
data, then applying K-Means Clustering and Market Basket Analysis to
customer and merchant data to surface insights that could inform
marketing strategy. Here, it's rebuilt as a standalone, runnable pipeline
against synthetic (but realistically messy) transaction data.

## What it does

1. **Cleaning** — strips stray whitespace, standardizes casing on
   customer IDs and product names, drops exact duplicate rows, and fills
   missing prices using the product's median price.
2. **Customer segmentation** — aggregates each customer's total spend,
   order count, and average basket value, scales the features, and runs
   K-Means clustering to group customers into spend/frequency segments.
3. **Market basket analysis** — counts how often every pair of products
   appears in the same order, surfacing the strongest product
   associations.
4. **Outputs** — a cleaned CSV, a customer-segments CSV, a cluster
   scatter chart, and a top-product-pairs CSV.

## Running it

```bash
pip install -r requirements.txt

# optional: regenerate the sample data
python generate_sample_data.py

python pipeline.py sample_transactions.csv
```

## Input format

A CSV with five columns: `order_id, customer_id, product, quantity,
unit_price`. `generate_sample_data.py` produces a realistic messy
version of this (duplicates, missing prices, inconsistent text) so the
cleaning step has something real to do.

## Sample output

On the included sample data (1,697 raw transaction rows across 60
customers), the pipeline removes 25 duplicate rows, segments customers
into 3 clusters ranging from occasional low-spend buyers to frequent
high-spend customers, and identifies **Bluetooth Headphones + Wireless
Mouse** as the most common product pairing.

"""
Customer Data Cleaning & Insights Pipeline
--------------------------------------------
Takes raw, messy retail transaction data (duplicates, missing values,
inconsistent casing/whitespace) and:

  1. Cleans it: dedupes, standardizes IDs/text, handles missing prices
  2. Segments customers with K-Means clustering on spend behaviour
  3. Runs a simple market-basket co-occurrence analysis to find which
     products are most often bought together
  4. Saves a cleaned dataset, a cluster chart, and a text insights summary

Run:
    python pipeline.py sample_transactions.csv
"""

import sys
from itertools import combinations
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    before = len(df)

    # standardize text fields
    df["customer_id"] = df["customer_id"].str.strip().str.upper()
    df["product"] = df["product"].str.strip().str.title()

    # drop exact duplicate rows
    df = df.drop_duplicates()

    # handle missing prices: fill with the product's median price
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["unit_price"] = df.groupby("product")["unit_price"].transform(
        lambda x: x.fillna(x.median())
    )

    df["line_total"] = df["unit_price"] * df["quantity"]

    after = len(df)
    print(f"Cleaned data: {before} rows -> {after} rows "
          f"({before - after} duplicates removed)")
    return df


def segment_customers(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    agg = df.groupby("customer_id").agg(
        total_spend=("line_total", "sum"),
        num_orders=("order_id", "nunique"),
        avg_basket_value=("line_total", "mean"),
    ).reset_index()

    features = agg[["total_spend", "num_orders", "avg_basket_value"]]
    scaled = StandardScaler().fit_transform(features)

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    agg["cluster"] = km.fit_predict(scaled)

    return agg


def market_basket(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    pairs = Counter()
    for _, basket in df.groupby("order_id")["product"]:
        items = sorted(set(basket))
        for a, b in combinations(items, 2):
            pairs[(a, b)] += 1

    result = pd.DataFrame(
        [(a, b, count) for (a, b), count in pairs.items()],
        columns=["product_a", "product_b", "times_bought_together"],
    ).sort_values("times_bought_together", ascending=False)

    return result.head(top_n)


def plot_clusters(agg: pd.DataFrame, out_path: str = "cluster_chart.png"):
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(
        agg["num_orders"], agg["total_spend"],
        c=agg["cluster"], cmap="viridis", s=70, alpha=0.85
    )
    ax.set_xlabel("Number of Orders")
    ax.set_ylabel("Total Spend ($)")
    ax.set_title("Customer Segments by Order Frequency and Spend")
    legend = ax.legend(*scatter.legend_elements(), title="Cluster")
    ax.add_artist(legend)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print(f"Cluster chart saved to {out_path}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_transactions.csv"
    df = load_and_clean(path)
    df.to_csv("cleaned_transactions.csv", index=False)
    print("Cleaned data saved to cleaned_transactions.csv")

    agg = segment_customers(df)
    agg.to_csv("customer_segments.csv", index=False)

    print("\n--- Customer Segment Summary ---")
    print(agg.groupby("cluster")[["total_spend", "num_orders", "avg_basket_value"]]
          .mean().round(2).to_string())
    print(f"\nCustomers per segment:\n{agg['cluster'].value_counts().sort_index().to_string()}")

    plot_clusters(agg)

    print("\n--- Top Product Pairs Bought Together ---")
    pairs = market_basket(df)
    print(pairs.to_string(index=False))
    pairs.to_csv("product_pairs.csv", index=False)


if __name__ == "__main__":
    main()

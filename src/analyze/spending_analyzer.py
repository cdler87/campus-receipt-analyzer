from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass
class SpendingAnalyzer:
    def monthly_totals(self, df: pd.DataFrame) -> pd.DataFrame:
        temp = df.dropna(subset=["timestamp", "total"]).copy()
        temp["month"] = temp["timestamp"].dt.to_period("M")
        monthly = temp.groupby("month", as_index=False)["total"].sum()
        monthly["month"] = monthly["month"].dt.to_timestamp()
        return monthly

    def category_breakdown(self, df: pd.DataFrame) -> pd.DataFrame:
        temp = df.dropna(subset=["category", "item_price"]).copy()
        return temp.groupby("category", as_index=False)["item_price"].sum()

    def top_items(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        temp = df.dropna(subset=["item_name"]).copy()
        return (
            temp.groupby("item_name", as_index=False)
            .agg(order_count=("item_name", "count"), total_spent=("item_price", "sum"))
            .sort_values("order_count", ascending=False)
            .head(n)
        )

    def average_order_value(self, df: pd.DataFrame) -> float:
        dedup = df.drop_duplicates(subset=["message_id"])
        return float(dedup["total"].dropna().mean()) if "total" in dedup else 0.0

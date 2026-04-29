from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import pandas as pd


@dataclass
class ReceiptCleaner:
    def normalize_item_name(self, item_name: str) -> str:
        if not item_name:
            return ""
        return item_name.strip().lower()

    def standardize_timestamp(self, ts: str):
        if not ts:
            return None
        try:
            return pd.to_datetime(ts)
        except Exception:
            return None

    def clean_receipts(self, parsed_receipts: List[Dict]) -> pd.DataFrame:
        rows = []
        for receipt in parsed_receipts:
            base = {
                "message_id": receipt.get("message_id"),
                "vendor": receipt.get("vendor"),
                "timestamp": self.standardize_timestamp(receipt.get("timestamp")),
                "location": receipt.get("location"),
                "subtotal": receipt.get("subtotal"),
                "tax": receipt.get("tax"),
                "total": receipt.get("total"),
                "parse_success": receipt.get("parse_success"),
            }
            items = receipt.get("items", [])
            if not items:
                rows.append({**base, "item_name": None, "quantity": None, "item_price": None})
                continue
            for item in items:
                rows.append({
                    **base,
                    "item_name": self.normalize_item_name(item.get("name")),
                    "quantity": item.get("quantity") or 1,
                    "item_price": item.get("price"),
                })
        df = pd.DataFrame(rows)
        return self.deduplicate(df)

    def deduplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        if "message_id" in df.columns:
            return df.drop_duplicates(subset=["message_id", "item_name", "item_price"])
        return df

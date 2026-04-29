from __future__ import annotations

from typing import Dict, List
import pandas as pd


def classify_error(pred: Dict, gold: Dict) -> str:
    if not pred.get("parse_success", False):
        return "json_or_schema_failure"
    if pred.get("total") != gold.get("total"):
        return "total_mismatch"
    if pred.get("timestamp") != gold.get("timestamp"):
        return "timestamp_mismatch"
    if pred.get("location") != gold.get("location"):
        return "location_mismatch"
    if pred.get("items") != gold.get("items"):
        return "item_extraction_mismatch"
    return "correct"


def build_error_report(preds: List[Dict], golds: List[Dict]) -> pd.DataFrame:
    rows = []
    for pred, gold in zip(preds, golds):
        rows.append({
            "message_id": pred.get("message_id"),
            "error_type": classify_error(pred, gold),
            "pred_total": pred.get("total"),
            "gold_total": gold.get("total"),
            "pred_location": pred.get("location"),
            "gold_location": gold.get("location"),
        })
    return pd.DataFrame(rows)

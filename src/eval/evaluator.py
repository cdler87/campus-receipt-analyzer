from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from src.eval.error_analysis import build_error_report
from src.eval.metrics import field_accuracy, parse_success_rate, receipt_exact_match_rate


@dataclass
class Evaluator:
    def evaluate_parser(self, preds: List[Dict], golds: List[Dict]) -> Dict:
        return {
            "vendor_accuracy": field_accuracy(preds, golds, "vendor"),
            "timestamp_accuracy": field_accuracy(preds, golds, "timestamp"),
            "location_accuracy": field_accuracy(preds, golds, "location"),
            "total_accuracy": field_accuracy(preds, golds, "total"),
            "exact_match_rate": receipt_exact_match_rate(preds, golds),
            "parse_success_rate": parse_success_rate(preds),
        }

    def build_error_report(self, preds: List[Dict], golds: List[Dict]):
        return build_error_report(preds, golds)

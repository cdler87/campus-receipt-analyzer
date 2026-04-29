from __future__ import annotations

from typing import Dict, List


def field_accuracy(preds, golds, field):
    correct = 0
    total = len(preds)

    for p, g in zip(preds, golds):
        pred_val = p.get(field)
        gold_val = g.get(field)

        if isinstance(pred_val, str):
            pred_val = pred_val.strip().lower()
        if isinstance(gold_val, str):
            gold_val = gold_val.strip().lower()

        if pred_val == gold_val:
            correct += 1

    return correct / total if total > 0 else 0


def receipt_exact_match_rate(preds: List[Dict], golds: List[Dict]) -> float:
    if not preds or not golds:
        return 0.0
    total = min(len(preds), len(golds))
    exact = 0
    for pred, gold in zip(preds, golds):
        comparable_pred = {k: v for k, v in pred.items() if k not in {"raw_model_output", "parse_success"}}
        comparable_gold = {k: v for k, v in gold.items() if k not in {"raw_model_output", "parse_success"}}
        if comparable_pred == comparable_gold:
            exact += 1
    return exact / total if total else 0.0


def parse_success_rate(preds: List[Dict]) -> float:
    if not preds:
        return 0.0
    return sum(1 for p in preds if p.get("parse_success")) / len(preds)

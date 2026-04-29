from __future__ import annotations

from typing import Dict, List
import json
import pandas as pd

from config.prompts import ZERO_SHOT_PROMPT, FEW_SHOT_PROMPT, STRICT_JSON_PROMPT
from src.parse.receipt_parser import ReceiptParser
from src.eval.metrics import field_accuracy, parse_success_rate, receipt_exact_match_rate

PROMPT_VARIANTS = {
    "zero_shot": ZERO_SHOT_PROMPT,
    "strict_json": STRICT_JSON_PROMPT,
    "few_shot": FEW_SHOT_PROMPT,
}

def _coerce_predictions(raw_preds: list[dict], emails: list[dict]) -> list[dict]:
    output: list[dict] = []
    for raw, email in zip(raw_preds, emails):
        parsed = {}
        try:
            parsed = json.loads(raw.get("raw_model_output", "{}"))
        except:
            parsed = {}

        parsed["message_id"] = email["message_id"]
        parsed["parse_success"] = bool(parsed)

        output.append(parsed)
    return output


def run_prompt_comparison(
    parser: ReceiptParser,
    eval_emails: List[Dict],
    gold_labels: List[Dict],
) -> pd.DataFrame:
    rows = []

    gold_map = {g["message_id"]: g for g in gold_labels}

    for name, template in PROMPT_VARIANTS.items():
        raw_preds = []

        for email in eval_emails:
            if "{email_text}" in template:
                prompt = parser.build_prompt(email.get("body_text", ""), template)
            else:
                prompt = email.get("body_text", "")
            raw_preds.append({"raw_model_output": parser.call_llm(prompt)})

        preds = _coerce_predictions(raw_preds, eval_emails)

        print("\nPRED IDS:")
        for p in preds:
            print(p.get("message_id"))

        print("\nGOLD IDS:")
        for g in gold_labels:
            print(g.get("message_id"))

        aligned_preds = []
        aligned_golds = []

        for p in preds:
            mid = p.get("message_id")
            if mid in gold_map:
                aligned_preds.append(p)
                aligned_golds.append(gold_map[mid])

        print("\nDEBUG SAMPLE:")
        print("PRED:", aligned_preds[0] if aligned_preds else None)
        print("GOLD:", aligned_golds[0] if aligned_golds else None)

        rows.append({
            "prompt_variant": name,
            "vendor_accuracy": field_accuracy(aligned_preds, aligned_golds, "vendor"),
            "total_accuracy": field_accuracy(aligned_preds, aligned_golds, "total"),
            "parse_success_rate": parse_success_rate(preds),
            "exact_match_rate": receipt_exact_match_rate(aligned_preds, aligned_golds),
        })

    return pd.DataFrame(rows)

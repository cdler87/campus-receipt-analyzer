from src.utils.io_utils import load_jsonl, load_json
from src.eval.evaluator import Evaluator

from config.settings import PARSED_RECEIPTS_PATH

def main():
    preds = load_jsonl(PARSED_RECEIPTS_PATH)
    golds = load_json("data/eval/ground_truth.json")

    evaluator = Evaluator()
    results = evaluator.evaluate_parser(preds, golds)

    print("\nEVALUATION RESULTS:")
    for k, v in results.items():
        print(f"{k}: {v:.2f}")
    
    error_df = evaluator.build_error_report(preds, golds)
    print("\nERROR REPORT:")
    print(error_df)

if __name__ == "__main__":
    main()

# from pathlib import Path
# import pandas as pd

# from config.settings import ERROR_REPORT_PATH, EVAL_RESULTS_PATH
# from src.eval.evaluator import Evaluator
# from src.utils.io_utils import load_json, save_json


# GOLD_PATH = Path("data/processed/gold_receipts.json")
# PRED_PATH = Path("data/interim/pred_receipts_eval.json")


# def main() -> None:
#     gold = load_json(GOLD_PATH)
#     preds = load_json(PRED_PATH)

#     evaluator = Evaluator()
#     results = evaluator.evaluate_parser(preds, gold)
#     save_json(results, EVAL_RESULTS_PATH)

#     error_df = evaluator.build_error_report(preds, gold)
#     error_df.to_csv(ERROR_REPORT_PATH, index=False)

#     print(results)
#     print(f"Saved error report to {ERROR_REPORT_PATH}")


# if __name__ == "__main__":
#     main()

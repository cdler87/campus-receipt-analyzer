from src.parse.receipt_parser import ReceiptParser
from src.parse.prompt_experiments import run_prompt_comparison
from src.utils.io_utils import load_json, load_jsonl
from config.settings import OPENAI_API_KEY, OPENAI_MODEL, RAW_EMAILS_PATH

def main():
    parser = ReceiptParser(api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)

    emails = [
    e for e in load_json(RAW_EMAILS_PATH)
    if e["message_id"] in [
        "#107936480 Receipt.eml",
        "#106427748 Receipt.eml",
        "#112401518 Receipt.eml"
    ]
]
    gold = load_json("data/eval/ground_truth.json")

    df = run_prompt_comparison(parser, emails, gold)

    print("\nPROMPT COMPARISON:")
    print(df)

if __name__ == "__main__":
    main()
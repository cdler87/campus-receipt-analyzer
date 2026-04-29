from config.settings import OPENAI_API_KEY, OPENAI_MODEL, PARSED_RECEIPTS_PATH, RAW_EMAILS_PATH
from src.parse.receipt_parser import ReceiptParser
from src.utils.io_utils import load_json, save_jsonl


def main() -> None:
    emails = load_json(RAW_EMAILS_PATH)
    emails = emails[:20]
    parser = ReceiptParser(api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)
    parsed = parser.parse_batch(emails)
    save_jsonl(parsed, PARSED_RECEIPTS_PATH)
    print(f"Saved {len(parsed)} parsed receipts to {PARSED_RECEIPTS_PATH}")


if __name__ == "__main__":
    main()

from config.settings import CLEAN_RECEIPTS_PATH, PARSED_RECEIPTS_PATH
from src.preprocess.categorizer import PurchaseCategorizer
from src.preprocess.cleaner import ReceiptCleaner
from src.utils.io_utils import load_jsonl


def main() -> None:
    parsed = load_jsonl(PARSED_RECEIPTS_PATH)
    cleaner = ReceiptCleaner()
    categorizer = PurchaseCategorizer()

    df = cleaner.clean_receipts(parsed)
    df["category"] = df["item_name"].apply(categorizer.categorize_item)
    df.to_csv(CLEAN_RECEIPTS_PATH, index=False)

    print(f"Saved cleaned data to {CLEAN_RECEIPTS_PATH}")


if __name__ == "__main__":
    main()

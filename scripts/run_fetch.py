from config.settings import GRAPH_CLIENT_ID, GRAPH_CLIENT_SECRET, GRAPH_TENANT_ID, RAW_EMAILS_PATH
from src.fetch.eml_loader import load_eml_emails
from src.utils.io_utils import save_json


def main() -> None:
    from src.fetch.eml_loader import load_eml_emails
from src.preprocess.filter_receipts import filter_receipts
from src.utils.io_utils import save_json
from config.settings import RAW_EMAILS_PATH

def main():
    folder_path = "data/exported_emails"

    print("Loading .eml files...")
    emails = load_eml_emails(folder_path)

    print(f"Loaded {len(emails)} emails")

    filtered = filter_receipts(emails)

    print(f"Filtered down to {len(filtered)} receipt emails")

    save_json(filtered, RAW_EMAILS_PATH)

    print("Saved filtered emails.")

if __name__ == "__main__":
    main()

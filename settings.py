from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_CLIENT_ID = os.getenv("GRAPH_CLIENT_ID", "")
GRAPH_TENANT_ID = os.getenv("GRAPH_TENANT_ID", "")
GRAPH_CLIENT_SECRET = os.getenv("GRAPH_CLIENT_SECRET", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

RAW_EMAILS_PATH = RAW_DIR / "receipts_raw.json"
PARSED_RECEIPTS_PATH = INTERIM_DIR / "parsed_receipts.jsonl"
CLEAN_RECEIPTS_PATH = PROCESSED_DIR / "receipts_clean.csv"
EVAL_RESULTS_PATH = PROCESSED_DIR / "evaluation_results.json"
ERROR_REPORT_PATH = PROCESSED_DIR / "error_report.csv"

from config.settings import OPENAI_API_KEY

print(OPENAI_API_KEY)
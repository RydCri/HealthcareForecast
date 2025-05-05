from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
ADMISSIONS_DIR = DATA_DIR / "admissions"

FORECAST_OUTPUT_PATH = BASE_DIR / "forecasts"
MODELS_DIR = BASE_DIR / "model"

BASE_DIR = Path(__file__).resolve().parents[2]

def admissions_path(date: str = None):
    date_str = date or datetime.today().strftime("%Y-%m-%d")
    path = BASE_DIR / "data" / "admissions" / f"admissions_{date_str}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)
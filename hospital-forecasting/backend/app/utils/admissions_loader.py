import pandas as pd
import os
from pathlib import Path

# TODO: change back to airflow
BASE_DIR = Path(__file__).resolve().parents[3]
ADMISSIONS_DIR = BASE_DIR / "data/hospital"

def load_latest_admissions_data():
    csvs = sorted(ADMISSIONS_DIR.glob("*admissions.csv"), reverse=True)
    if not csvs:
        raise FileNotFoundError("No admissions CSVs found.")
    return pd.read_csv(csvs[0])

import pandas as pd
from pathlib import Path

ADMISSIONS_DIR = Path("/opt/airflow/data/admissions")

def load_latest_admissions_data():
    csvs = sorted(ADMISSIONS_DIR.glob("*admissions_2025.csv"), reverse=True)
    if not csvs:
        raise FileNotFoundError("No admissions CSVs found.")
    return pd.read_csv(csvs[0])

import pandas as pd
from pathlib import Path

STAFFING_DIR = Path("/opt/airflow/data/staffing")

def load_latest_staffing_data():
    csvs = sorted(STAFFING_DIR.glob("*staffing.csv"), reverse=True)
    if not csvs:
        raise FileNotFoundError("No staffing CSVs found.")
    return pd.read_csv(csvs[0])

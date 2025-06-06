import pandas as pd
from pathlib import Path

PROCEDURES_DIR = Path("/opt/airflow/data/procedures")


def load_latest_procedures_data():
    csvs = sorted(PROCEDURES_DIR.glob("*procedures*.csv"), reverse=True)
    if not csvs:
        raise FileNotFoundError("No procedures CSVs found.")
    return pd.read_csv(csvs[0])

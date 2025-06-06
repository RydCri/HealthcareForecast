import pandas as pd
from pathlib import Path

BEDS_DIR = Path("/opt/airflow/data/bed_occupancy")


def load_latest_beds_data():
    csvs = sorted(BEDS_DIR.glob("*bed_occupancy*.csv"), reverse=True)
    if not csvs:
        raise FileNotFoundError("No bed occupancy CSVs found.")
    return pd.read_csv(csvs[0])

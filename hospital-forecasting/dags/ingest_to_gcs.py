from datetime import datetime
from airflow import DAG
from airflow.decorators import task
import pandas as pd
from src.utils.paths import ADMISSIONS_DIR, BASE_DIR
from src.utils.gcs import upload_blob
import logging

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
        dag_id="ingest_admissions_data",
        default_args=default_args,
        description="Generate and upload mock hospital admissions data",
        schedule_interval="@daily",  # or None for manual trigger
        start_date=datetime(2025, 5, 1),
        catchup=False,
        tags=["hospital", "gcs", "etl"],
) as dag:

    @task
    def generate_mock_admissions():
        today = datetime.today().strftime("%Y-%m-%d")
        data = {
            "admission_id": [f"A{str(i).zfill(4)}" for i in range(1, 101)],
            "admission_date": [today] * 100,
            "department": ["ER"] * 50 + ["ICU"] * 50,
            "severity_score": pd.np.random.uniform(0, 10, 100),
        }
        df = pd.DataFrame(data)
        path = ADMISSIONS_DIR(today)
        df.to_csv(path, index=False)
        logging.info(f"Saved CSV to {path}")
        return path

    @task
    def upload_to_gcs(path: str):
        destination = f"admissions/{path.split('/')[-1]}"
        upload_blob(path, destination)

    # DAG flow
    local_path = generate_mock_admissions()
    upload_to_gcs(local_path)

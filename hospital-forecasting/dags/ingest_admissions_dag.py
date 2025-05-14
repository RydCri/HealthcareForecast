import os
import pandas as pd
from airflow import DAG
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from google.api_core.exceptions import Forbidden

# load vars from .env
load_dotenv()

BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
SOURCE_BLOB = "data/admissions/admissions_2025.csv"  # no trailing / when fetching from GCS
# DEST_PATH = "/opt/airflow/include/admissions_2025.csv"
DEST_PATH = "/opt/airflow/data/admissions/admissions_2025.csv"

# GCP_CREDS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # Can be set manually in Airflow > Admin > Connections > google_cloud_default

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "airflow")
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")

def download_from_gcs():
    hook = GCSHook(gcp_conn_id="google_cloud_default")
    client = hook.get_conn()
    bucket = client.bucket("your-bucket-name")
    blob = bucket.blob("admissions/admissions_2025.csv")

    try:
        blob.download_to_filename("/opt/airflow/data/admissions/admissions_2025.csv")
        print("File downloaded from GCS successfully")
    except Forbidden as e:
        raise AirflowException(f"GCS download failed: {e.message}")


def load_into_postgres():
    df = pd.read_csv(DEST_PATH)
    engine = create_engine(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    df.to_sql("admissions", engine, if_exists="replace", index=False)
    print("Data loaded into Postgres!")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 5, 1),
    "retries": 1,
}

with DAG(
        dag_id="ingest_admissions",
        default_args=default_args,
        schedule_interval="@daily",
        catchup=False,
        tags=["gcs", "hospital"],
) as dag:

    ingest_task = PythonOperator(
        task_id="download_admissions_csv",
        python_callable=download_from_gcs,
    )

    load_task = PythonOperator(
        task_id="load_csv_into_postgres",
        python_callable=load_into_postgres,
    )

    ingest_task >> load_task

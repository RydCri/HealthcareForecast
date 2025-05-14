import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from google.cloud import storage
from sqlalchemy import create_engine
from dotenv import load_dotenv

# load vars from .env
load_dotenv()

BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
SOURCE_BLOB = "data/admissions/admissions_2025.csv"  # no trailing / when fetching from GCS
DEST_PATH = "/opt/airflow/include/admissions_2025.csv"
GCP_CREDS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "airflow")
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")

def download_from_gcs():
    print(f"GCP_CREDS_JSON: {GCP_CREDS_JSON}")
    print(f"BUCKET_NAME: {BUCKET_NAME}")
    print(f"SOURCE_BLOB: {SOURCE_BLOB}")
    print(f"DEST_PATH: {DEST_PATH}")

    client = storage.Client.from_service_account_json(GCP_CREDS_JSON)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(SOURCE_BLOB)

    if not blob.exists(client):
        raise FileNotFoundError(f"The blob '{SOURCE_BLOB}' does not exist in bucket '{BUCKET_NAME}'")

    blob.download_to_filename(DEST_PATH)
    print(f"Downloaded {SOURCE_BLOB} to {DEST_PATH}")

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

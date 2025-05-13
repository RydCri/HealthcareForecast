import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from google.cloud import storage
from sqlalchemy import create_engine

# Load env vars from .env if needed
from dotenv import load_dotenv
load_dotenv()

BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
DEST_PATH = "/opt/airflow/include/admissions_2025.csv"
SOURCE_BLOB = "admissions/admissions_2025.csv"
GCP_CREDS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def download_from_gcs():
    client = storage.Client.from_service_account_json(GCP_CREDS_JSON)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(SOURCE_BLOB)
    blob.download_to_filename(DEST_PATH)
    print(f"Downloaded {SOURCE_BLOB} to {DEST_PATH}")

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
        task_id="download_admissions_from_gcs",
        python_callable=download_from_gcs,
    )

    ingest_task


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "airflow")
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")



def load_into_postgres():
    df = pd.read_csv(DEST_PATH)

    engine = create_engine(
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )

    df.to_sql("admissions", engine, if_exists="replace", index=False)
    print("Data loaded into Postgres!")

ingest_task = PythonOperator(
    task_id="download_admissions_csv",
    python_callable=download_from_gcs,
)

load_task = PythonOperator(
    task_id="load_csv_into_postgres",
    python_callable=load_into_postgres,
)

ingest_task >> load_task

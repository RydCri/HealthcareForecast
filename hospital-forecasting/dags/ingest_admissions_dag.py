import os
import pandas as pd
from airflow import DAG
from datetime import datetime
from sqlalchemy import create_engine
from utils.paths import ADMISSIONS_DIR
from dotenv import load_dotenv
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from google.api_core.exceptions import Forbidden

# load vars from .env
load_dotenv()

GCS_BUCKET = os.getenv("GCS_BUCKET_NAME")
SOURCE_BLOB = "data/admissions/admissions_2025.csv"  # no trailing / when fetching from GCS
DEST_PATH = "/opt/airflow/data/admissions/admissions_2025.csv"

# Can be set manually in Airflow > Admin > Connections > google_cloud_default
# GCP_CREDS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "airflow")
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")

GCS_OBJECT = "admissions/admissions_2025.csv"
LOCAL_TARGET = os.path.join(ADMISSIONS_DIR, "admissions_2025.csv")


def download_from_gcs():
    try:
        hook = GCSHook(gcp_conn_id="google_cloud_default")
        # client can use GCP_CREDS_JSON if preferred
        client = hook.get_conn()
        bucket = client.bucket(GCS_BUCKET)
        blob = bucket.blob(GCS_OBJECT)

        blob.download_to_filename(LOCAL_TARGET)
        print("Downloaded from GCS successfully.")

    except Forbidden as e:
        print(f"GCS download failed: 403 {e}")
        # TODO: Using backup file if GCS triggers 403 ( billing acct issue )
        if os.path.exists(LOCAL_TARGET):
            print(f"Using local backup file at {LOCAL_TARGET}")
        else:
            raise AirflowException("Neither GCS download nor local backup is available.")


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

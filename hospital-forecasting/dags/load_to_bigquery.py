# dags/load_to_bigquery.py
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime

# GCS_URI = "gs://your-bucket/admissions_cleaned.parquet"
# BQ_TABLE = "your_project.your_dataset.admissions_cleaned"

GCS_URI = "gs://hospital-forecast-dev/admissions_cleaned.parquet"
BQ_TABLE = "hospital-forecast-dev.hospital_forecast.admissions_cleaned"


with DAG("load_to_bigquery",
         start_date=datetime(2023, 1, 1),
         schedule_interval="@daily",
         catchup=False) as dag:

    load_bq = BigQueryInsertJobOperator(
        task_id="load_cleaned_to_bq",
        configuration={
            "load": {
                "sourceUris": [GCS_URI],
                "destinationTable": {
                    "projectId": "your_project",
                    "datasetId": "your_dataset",
                    "tableId": "admissions_cleaned",
                },
                "sourceFormat": "PARQUET",
                "writeDisposition": "WRITE_TRUNCATE",
            }
        },
        location="US"
    )

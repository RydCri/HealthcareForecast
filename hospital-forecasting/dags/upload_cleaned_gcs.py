from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from utils.gcs import upload_cleaned_data_to_gcs

with DAG("upload_cleaned_to_gcs",
         start_date=datetime(2023, 1, 1),
         schedule_interval="@daily",
         catchup=False) as dag:

    upload_task = PythonOperator(
        task_id="upload_cleaned_data",
        python_callable=upload_cleaned_data_to_gcs,
    )

# dags/hospital_pipeline_dag.py

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from jobs.generate_admissions import generate_patient_admission
from jobs.upload_to_gcs import upload_blob
from jobs.load_to_bq import load_to_bigquery

with DAG(
        dag_id="hospital_resource_forecast",
        start_date=datetime(2025, 5, 1),
        schedule_interval="@daily",
        catchup=False,
        default_args={"retries": 1},
        tags=["hospital", "etl"],
) as dag:

    generate_task = PythonOperator(
        task_id="generate_admissions",
        python_callable=generate_patient_admission,
    )

    upload_task = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_blob,
        op_kwargs={"local_path": "data/admissions/admissions_2025.csv",
                   "blob_name": "data/admissions/admissions_2025.csv"}
    )

    load_task = PythonOperator(
        task_id="load_to_bq",
        python_callable=load_to_bigquery,
        op_kwargs={"blob_name": "data/admissions/admissions_2025.csv"}
    )

    generate_task >> upload_task >> load_task

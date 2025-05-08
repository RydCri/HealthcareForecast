# TODO: task and generate weekly forecast model
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.model.forecast import generate_and_store_forecast

with DAG("generate_forecast",
         start_date=datetime(2023, 1, 1),
         schedule_interval="@weekly",
         catchup=False) as dag:

    forecast_task = PythonOperator(
        task_id="generate_forecast_task",
        python_callable=generate_and_store_forecast,
    )
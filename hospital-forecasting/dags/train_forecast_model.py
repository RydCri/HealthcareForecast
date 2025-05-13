from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from model.train import train_admissions_model

with DAG("train_forecast_model",
         start_date=datetime(2023, 1, 1),
         schedule_interval="@weekly",
         catchup=False) as dag:

    train_model = PythonOperator(
        task_id="train_forecast_model_task",
        python_callable=train_admissions_model,
    )

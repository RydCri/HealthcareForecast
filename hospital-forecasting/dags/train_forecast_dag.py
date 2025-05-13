from airflow import DAG
import sys
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime
from model.train import train_model
from model.forecast import generate_and_store_forecast
from model.evaluate import evaluate_model_performance
from alerts.slack import send_slack_alert
print("PYTHONPATH: LOOK HERE", sys.path)

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
        dag_id="train_forecast_with_eval",
        default_args=default_args,
        schedule_interval="@daily",
        catchup=False,
        description="Train model, forecast, evaluate, and alert if poor performance",
        tags=["ml", "forecasting"],
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    no_alert = EmptyOperator(task_id="no_alert")

    @task
    def train_model_task():
        train_model()

    @task
    def forecast_task():
        generate_and_store_forecast()

    @task
    def evaluate_task() -> float:
        return evaluate_model_performance()

    def check_performance(mae: float):
        return "send_alert" if mae > 10 else "no_alert"

    check = BranchPythonOperator(
        task_id="check_performance",
        python_callable=check_performance,
        op_args=["{{ ti.xcom_pull(task_ids='evaluate_task') }}"],
    )

    @task
    def send_alert_task():
        send_slack_alert()

    # DAG flow
    start >> train_model_task() >> forecast_task() >> evaluate_task() >> check
    check >> [send_alert_task(), no_alert] >> end

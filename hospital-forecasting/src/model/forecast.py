import pandas as pd
import joblib
from sqlalchemy import create_engine
from google.cloud import bigquery
from prophet.serialize import model_from_json
from utils.paths import FORECAST_OUTPUT_PATH, MODELS_DIR

def generate_and_store_forecast():
    # Load trained model
    model_path = MODELS_DIR / "admissions_forecast_model.pkl"
    model = joblib.load(model_path)

    # Generate forecast
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    # Save to local CSV
    result.to_csv(FORECAST_OUTPUT_PATH, index=False)
    print(f"✅ Forecast saved to {FORECAST_OUTPUT_PATH}")

    # Postgres
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/airflow")
    result.to_sql("admissions_forecast", engine, if_exists="replace", index=False)
    print("✅ Forecast written to Postgres (table: admissions_forecast)")

    # BigQuery
    client = bigquery.Client()
    table_id = "your-project-id.dataset_id.admissions_forecast"
    job = client.load_table_from_dataframe(result, table_id, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"))
    job.result()  # Waits for job to complete
    print(f"✅ Forecast written to BigQuery ({table_id})")

import os
from dotenv import load_dotenv
from google.cloud import bigquery
load_dotenv()

def main():
    client = bigquery.Client()

    bucket = os.getenv("GCS_BUCKET")
    dataset = "hospital_forecast"
    table = "admissions_staging"
    uri = f"gs://{bucket}/data/admissions/admissions_2025.csv"

    table_id = f"{client.project}.{dataset}.{table}"

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()  # Wait for completion

    print(f"✅ Loaded GCS CSV to BigQuery table {table_id}")

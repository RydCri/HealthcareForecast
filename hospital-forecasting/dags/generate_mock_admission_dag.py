from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import random
from faker import Faker
import uuid
import os

# DAG config
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Output directory
ADMISSIONS_DIR = "/opt/airflow/data/admissions"
os.makedirs(ADMISSIONS_DIR, exist_ok=True)

fake = Faker()

DEPARTMENTS = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Oncology', 'Emergency', 'ICU']
SEVERITY_LEVELS = ['Mild', 'Moderate', 'Severe']
INSURANCE_TYPES = ['Government', 'Private', 'None']
DIAGNOSES = [
    'I10 - Hypertension', 'E11 - Type 2 Diabetes', 'J45 - Asthma',
    'K21 - GERD', 'C50 - Breast Cancer', 'R07 - Chest Pain', 'S72 - Hip Fracture'
]


def generate_patient_admission(n=1000, start_date="2024-01-01", end_date="2024-12-31"):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    delta_days = (end_dt - start_dt).days

    records = []
    for _ in range(n):
        admit_dt = start_dt + timedelta(days=random.randint(0, delta_days))
        record = {
            'patient_id': str(uuid.uuid4()),
            'admit_date': admit_dt.strftime("%Y-%m-%d"),
            'dept': random.choice(DEPARTMENTS),
            'severity': random.choices(SEVERITY_LEVELS, weights=[0.5, 0.35, 0.15])[0],
            'diagnosis': random.choice(DIAGNOSES),
            'age': random.randint(1, 99),
            'insurance_type': random.choices(INSURANCE_TYPES, weights=[0.6, 0.3, 0.1])[0]
        }
        records.append(record)

    return pd.DataFrame(records)


def save_admissions_csv(**kwargs):
    df = generate_patient_admission(n=1000)
    date_prefix = datetime.now().strftime("%m-%d")
    filename = f"{date_prefix}_admissions_2025.csv"
    filepath = os.path.join(ADMISSIONS_DIR, filename)
    df.to_csv(filepath, index=False)
    print(f"✅ Generated {len(df)} rows → {filepath}")


with DAG(
        dag_id='generate_mock_admissions',
        default_args=default_args,
        schedule_interval='@daily',
        catchup=False,
        tags=['mock', 'admissions', 'csv'],
) as dag:

    generate_csv = PythonOperator(
        task_id='generate_mock_admissions_csv',
        python_callable=save_admissions_csv,
        provide_context=True
    )

    generate_csv

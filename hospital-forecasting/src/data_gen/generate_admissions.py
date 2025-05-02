from pathlib import Path
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import uuid
BASE_DIR = Path(__file__).resolve().parent.parent.parent
fake = Faker()

DEPARTMENTS = [
    'Cardiology', 'Neurology', 'Orthopedics',
    'Pediatrics', 'Oncology', 'Emergency', 'ICU'
]

SEVERITY_LEVELS = ['Mild', 'Moderate', 'Severe']
INSURANCE_TYPES = ['Government', 'Private', 'None']
DIAGNOSES = [
    'I10 - Hypertension', 'E11 - Type 2 Diabetes',
    'J45 - Asthma', 'K21 - GERD',
    'C50 - Breast Cancer', 'R07 - Chest Pain',
    'S72 - Hip Fracture'
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


if __name__ == "__main__":
    df = generate_patient_admission(n=1000)
    df.to_csv(f"{BASE_DIR}/data/admissions/admissions_2025.csv", index=False)
    print(f"Generated {len(df)} rows → data/admissions/admissions_2025.csv")

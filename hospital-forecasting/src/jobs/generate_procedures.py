import pandas as pd
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta
from collections import defaultdict
from .generate_admissions import generate_patient_admission

fake = Faker()

DEPARTMENTS = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Oncology', 'Emergency', 'ICU']
PROCEDURES = ['Appendectomy', 'MRI Scan', 'X-Ray', 'ECG', 'Colonoscopy', 'CT Scan', 'Blood Test', 'Chemotherapy', 'Physical Therapy', 'Dialysis']
ROLES = ["Doctor", "Nurse", "Technician", "Admin"]

ICU_BED_IDS = [f"ICU-{i:03}" for i in range(10)]
GEN_BED_IDS = [f"BED-{i:03}" for i in range(100, 200)]
ALL_BED_IDS = ICU_BED_IDS + GEN_BED_IDS


def generate_doctors(n=20):
    return [fake.name() for _ in range(n)]


# Call admission generator or use .csv to df pandas method

def generate_procedures_billing(admissions_df, doctors):
    records = []
    for _, row in admissions_df.iterrows():
        n_procedures = random.randint(1, 5)
        base_date = datetime.strptime(row['admit_date'], "%Y-%m-%d")
        for _ in range(n_procedures):
            proc_date = base_date + timedelta(days=random.randint(-30, 30))
            records.append({
                'procedure_id': str(uuid.uuid4()),
                'patient_id': row['patient_id'],
                'procedure': random.choice(PROCEDURES),
                'cost': round(random.uniform(100, 10000), 2),
                'performed_by': random.choice(doctors),
                'date': proc_date.strftime('%Y-%m-%d')
            })
    return pd.DataFrame(records)


def generate_staffing_schedule(days=30):
    schedule = []
    staff_pool = defaultdict(list)

    for dept in DEPARTMENTS:
        for i in range(5):  # 5 unique staff per department
            for role in ROLES:
                staff_id = str(uuid.uuid4())
                staff_pool[dept].append({'staff_id': staff_id, 'role': role})

    start_date = datetime.today()
    for i in range(days):
        shift_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        for dept in DEPARTMENTS:
            scheduled_ids = set()
            needed_roles = ["Doctor"] + ["Nurse"] * 2
            for role in needed_roles:
                candidates = [s for s in staff_pool[dept] if s['role'] == role and s['staff_id'] not in scheduled_ids]
                if candidates:
                    staff = random.choice(candidates)
                    schedule.append({
                        'staff_id': staff['staff_id'],
                        'role': staff['role'],
                        'department': dept,
                        'shift_date': shift_date,
                        'hours': random.choice([8, 12])
                    })
                    scheduled_ids.add(staff['staff_id'])
    return pd.DataFrame(schedule)


def generate_bed_occupancy(admissions_df):
    bed_assignments = {bed_id: [] for bed_id in ALL_BED_IDS}
    occupancy_records = []

    for _, row in admissions_df.iterrows():
        is_icu = random.random() < 0.2
        bed_pool = ICU_BED_IDS if is_icu else GEN_BED_IDS
        admit_time = datetime.strptime(row['admit_date'], "%Y-%m-%d") + timedelta(hours=random.randint(0, 23))
        duration = timedelta(hours=random.randint(12, 72))
        end_time = admit_time + duration

        assigned_bed = None
        for bed in bed_pool:
            overlaps = any(
                not (end_time <= occ[0] or admit_time >= occ[1])
                for occ in bed_assignments[bed]
            )
            if not overlaps:
                assigned_bed = bed
                bed_assignments[bed].append((admit_time, end_time))
                break

        if assigned_bed:
            occupancy_records.append({
                'bed_id': assigned_bed,
                'dept': row['dept'],
                'patient_id': row['patient_id'],
                'start_time': admit_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'is_ICU': is_icu
            })
    return pd.DataFrame(occupancy_records)

"""

    # Example:
    
     admissions_df = generate_patient_admission()
     doctors = generate_doctors()
     procedures_df = generate_procedures_billing(admissions_df, doctors)
     staffing_df = generate_staffing_schedule(days=30)
     beds_df = generate_bed_occupancy(admissions_df)
     
"""
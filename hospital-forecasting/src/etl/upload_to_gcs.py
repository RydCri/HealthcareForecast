from google.cloud import storage
from ..utils.paths import BASE_DIR
import os

def upload_to_gcs(bucket_name, source_file_path, destination_blob_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_path)

    blob.upload_from_filename(source_file_path)
    print(f"✅ Uploaded {source_file_path} to gs://{bucket_name}/{destination_blob_path}")


if __name__ == "__main__":
    # Local CSV
    local_path = f"{BASE_DIR}/data/admissions/admissions_2025.csv"

    # GCS
    bucket = "hospital-data-forecasting"
    gcs_path = f"{BASE_DIR}/admissions/admissions_2025.csv"

    if os.path.exists(local_path):
        upload_to_gcs(bucket, local_path, gcs_path)
    else:
        print(f"File not found: {local_path}")

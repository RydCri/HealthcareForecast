from google.cloud import storage
from utils.paths import BASE_DIR, ADMISSIONS_DIR
from utils.gcs import upload_blob
import os


def upload_to_gcs(bucket_name, source_file_path, destination_blob_path):
    client = storage.Client()
    bucket = client.bucket(os.getenv("GCS_BUCKET"))
    blob = bucket.blob(destination_blob_path)

    blob.upload_from_filename(source_file_path)
    print(f"✅ Uploaded {source_file_path} to gs://{bucket_name}/{destination_blob_path}")


if __name__ == "__main__":
    # local .csv
    file_path = ADMISSIONS_DIR / "admissions_2025.csv"
    # GCS Bucket
    blob_name = "data/admissions/admissions_2025.csv"
    upload_blob(local_path=str(file_path), blob_name=blob_name)

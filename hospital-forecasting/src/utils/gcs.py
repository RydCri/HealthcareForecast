import os
from google.cloud import storage
from dotenv import load_dotenv
from utils.paths import CLEANED_ADMISSIONS_PATH

# Load environment variables
load_dotenv()

def init_gcs_client():
    # Initialize and return a GCS client and bucket object using env vars.
    # Requires GOOGLE_APPLICATION_CREDENTIALS and GCS_BUCKET to be set.
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    bucket_name = os.getenv("GCS_BUCKET")

    if not credentials_path or not bucket_name:
        raise ValueError("Missing GCS credentials or bucket name in environment variables.")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    return bucket


bucket_name = os.getenv("GCS_BUCKET_NAME")


def upload_blob(source_file_name, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"Uploaded {source_file_name} to gs://{bucket_name}/{destination_blob_name}")


def upload_cleaned_data_to_gcs():
    # Helper to upload the cleaned admissions data file to GCS.
    # Uses CLEANED_ADMISSIONS_PATH and uploads it to the root of the bucket with the same filename.

    source_file = str(CLEANED_ADMISSIONS_PATH)
    dest_blob_name = CLEANED_ADMISSIONS_PATH.name  # e.g., 'admissions_cleaned.parquet'

    upload_blob(source_file, dest_blob_name)
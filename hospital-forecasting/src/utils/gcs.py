import os
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_gcs_client():
    """
    Initialize and return a GCS client and bucket object using env vars.
    Requires GOOGLE_APPLICATION_CREDENTIALS and GCS_BUCKET to be set.
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    bucket_name = os.getenv("GCS_BUCKET")

    if not credentials_path or not bucket_name:
        raise ValueError("Missing GCS credentials or bucket name in environment variables.")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    return bucket


def upload_blob(local_path, blob_name, content_type="text/csv"):
    """
    Uploads a file to GCS.

    Args:
        local_path (str): Path to the local file to upload.
        blob_name (str): Desired name/path in the bucket (e.g. data/admissions/admissions_2025.csv).
        content_type (str): MIME type for the file. Defaults to "text/csv".
    """
    bucket = init_gcs_client()
    blob = bucket.blob(blob_name)

    blob.upload_from_filename(local_path, content_type=content_type)
    print(f"✅ Uploaded {local_path} to gs://{bucket.name}/{blob_name}")

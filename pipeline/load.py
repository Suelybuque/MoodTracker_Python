import os
from pathlib import Path

#AWS S3
try:
    import boto3
    from botocore.exceptions import NoCredentialsError
except ImportError:
    boto3= None

#Google Cloud Storage
try:
    from google.cloud import storage
except ImportError:
    storage= None

def upload_to_s3(file_path: str, bucked_name: str, object_name:str= None ):
    """
    Upload file to AWS S3
    """
    if boto3 is None:
        raise ImportError("boto 3 is required for AWS S3 upload.")
    object_name= object_name or Path(file_path).name
    s3_client= boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucked_name, object_name)
        print(f"Uploaded {file_path} to s3://{bucked_name}/{object_name}")
    except NoCredentialsError:
        print("AWS credentials not found!")

def upload_to_gcs(file_path: str, bucked_name: str, object_name:str= None):
    """"
    Upload file to google cloud storage
    """
    if storage is None:
         raise ImportError("google cloud storage is required for GCS upload")

    object_name= object_name or Path(file_path).name
    client= storage.Client()
    bucked= client.bucket(bucked_name)
    blob= bucked.blob(object_name)
    blob.upload_from_filename(file_path)
    print(f"Uploaded {file_path} to gs://{bucked_name}/{object_name}")
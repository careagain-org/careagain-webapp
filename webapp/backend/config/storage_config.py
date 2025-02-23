import boto3
from botocore.client import Config
import os
import logging

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MinIO connection details
STORAGE_URL = os.environ.get("MINIO_URL")
ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

# Create an S3 client
s3_client = boto3.client(
    "s3",
    endpoint_url=STORAGE_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version="s3v4"),
)

# # List buckets
# response = s3.list_buckets()
# print("Buckets:", [bucket["Name"] for bucket in response["Buckets"]])

# # Upload a file
# s3.upload_file("localfile.txt", "mybucket", "remote_file.txt")

# # Download a file
# s3.download_file("mybucket", "remote_file.txt", "downloaded_file.txt")

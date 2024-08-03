from fastapi import UploadFile
import boto3
from botocore.exceptions import NoCredentialsError
import os
import uuid

from ..core import settings, setup_logger

logger = setup_logger()

ACCESS_KEY = settings.s3_access_key
SECRET_KEY = settings.s3_secret_key
REGION_NAME = settings.s3_region_name
BUCKET_NAME = settings.s3_bucket_name

s3 = boto3.client('s3',
                  aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY,
                  region_name=REGION_NAME)


async def upload_to_s3(file: UploadFile, object_name=None):
    file_extension = os.path.splitext(file.filename)[1]

    unique_id = uuid.uuid4()
    object_name = f"{unique_id}{file_extension}"

    if object_name is None:
        object_name = f"{unique_id}_{object_name}{file_extension}"

    try:
        file_contents = await file.read()
        s3.put_object(Bucket=BUCKET_NAME, Key=object_name, Body=file_contents)

        file_url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{object_name}"

        logger.info(f"✅ File '{file.filename}' uploaded successfully as '{object_name}'. URL: {file_url}")

        return file_url
    except NoCredentialsError:
        logger.error("❌ Credentials not available. Please check your AWS credentials.")
        return None
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        return None
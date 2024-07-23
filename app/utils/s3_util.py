import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os

from ..core.logger_config import setup_logger

logger = setup_logger()

load_dotenv()

ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
SECRET_KEY = os.getenv('S3_SECRET_KEY')
REGION_NAME = os.getenv('S3_REGION_NAME')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def upload_to_s3(file_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

        object_name = f'AI/{object_name}'
        s3.upload_file(
            file_name, 
            BUCKET_NAME, 
            object_name, 
        )

        file_url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{object_name}"

        return file_url

    except FileNotFoundError:
        logger.error(f"The file '{file_name}' was not found")
        return file_name
    except NoCredentialsError:
        logger.error("Credentials not available. Please check your AWS credentials.")
        return file_name
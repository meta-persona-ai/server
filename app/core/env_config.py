from pydantic_settings import BaseSettings
from pydantic import ConfigDict, ValidationError
from dotenv import load_dotenv
import requests
import json
import sys

from .logger_config import setup_logger

load_dotenv()
logger = setup_logger()

class APIKeyValidationError(Exception):
    pass

class Settings(BaseSettings):
    # GOOGLE LOGIN
    google_client_id: str
    google_client_secret: str

    # S3
    s3_access_key: str
    s3_secret_key: str
    s3_region_name: str
    s3_bucket_name: str

    # JWT
    jwt_secret: str
    jwt_algorithm: str

    # DATABASE
    database_url: str

    # GEMINI
    google_api_key: str
    # google_api_key2: str
    # google_api_key3: str
    

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

def validate_google_api_key(google_api_key):
    result = requests.post(
        url= "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
        data=b'{"contents":[{"parts":[{"text":""}]}]}',
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": google_api_key
        }
    )
    if result.status_code != 200:
        message = json.loads(result.content).get('error').get('status')
        raise APIKeyValidationError(message)


try:
    settings = Settings()
    logger.info("📌 Settings loaded successfully.")
    validate_google_api_key(settings.google_api_key)
    logger.info("📌 Google API key validation passed.")
except ValidationError as e:
    logger.error("❌ Error loading settings:")
    for error in e.errors():
        loc = ".".join(str(loc) for loc in error['loc'])
        msg = error['msg']
        logger.error(f" - {loc}: {msg}")
    sys.exit(1)
except APIKeyValidationError as e:
    logger.error(f"❌ API key validation failed: {e}")
    sys.exit(1)
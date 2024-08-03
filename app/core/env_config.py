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

    # LANGCHAIN
    langchain_api_key: str
    langchain_tracing_v2: bool
    langchain_project: str

    # WEBHOOK
    WEBHOOK_URL: str | None = None
    SEND_WEBHOOK_MESSAGE: bool | None = False

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

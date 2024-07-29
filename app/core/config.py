from pydantic_settings import BaseSettings
from pydantic import ConfigDict, ValidationError
from dotenv import load_dotenv
import sys

from .logger_config import setup_logger

load_dotenv()
logger = setup_logger()

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
    

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )


try:
    settings = Settings()
    logger.info("📌 Settings loaded successfully.")
except ValidationError as e:
    logger.error("Error loading settings:")
    for error in e.errors():
        loc = ".".join(str(loc) for loc in error['loc'])
        msg = error['msg']
        logger.error(f" - {loc}: {msg}")
    sys.exit(1)
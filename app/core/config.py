from pydantic import ValidationError
import requests
import json
import sys

from .logger_config import setup_logger
from .env_config import Settings
from ..utils.webhook import env_loading_failure_message, validate_api_key_failure_message

logger = setup_logger()

class APIKeyValidationError(Exception):
    pass

def validate_google_api_key(google_api_key):
    print("=======================================")
    print(google_api_key)
    print("=======================================")
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
    print(settings.SEND_WEBHOOK_MESSAGE)
    logger.info("📌 Settings loaded successfully.")
    validate_google_api_key(settings.google_api_key)
    logger.info("📌 Google API key validation passed.")
except ValidationError as e:
    logger.error("❌ Error loading settings:")

    component_list = []
    for error in e.errors():
        loc = ".".join(str(loc) for loc in error['loc'])
        msg = error['msg']
        logger.error(f" - {loc}: {msg}")
        component_list.append(f"- `{loc}`: {msg}")

    env_loading_failure_message(component_list)

    sys.exit(1)
except APIKeyValidationError as e:
    logger.error(f"❌ Google API key validation failed: {e}")
    validate_api_key_failure_message()
    sys.exit(1)
import jwt
from jwt import PyJWKClient
from jose.exceptions import JWTError

from ..core.env_config import settings
from ..core.logger_config import setup_logger
from ..schemas.request.user_request_schema import UserCreate


logger = setup_logger()

def decode_id_token(id_token: str) -> UserCreate:
    """
    ID 토큰을 디코딩하고 검증하여 사용자 정보를 추출합니다.
    """
    jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
    jwks_client = PyJWKClient(jwks_url)

    signing_key = jwks_client.get_signing_key_from_jwt(id_token)

    options = {
        'verify_iat': True
    }

    try:
        user_info: dict = jwt.decode(id_token, signing_key.key, algorithms=["RS256"], audience=settings.google_client_id, options=options, leeway=30)
    except JWTError as e:
        logger.error(f"❌ JWT decoding error: {e}")
        return None

    user_data = {
        "user_id": int(user_info.get("sub")),
        "user_email": user_info.get("email"),
        "user_name": user_info.get("name"),
        "user_profile": user_info.get("picture"),
    }
    user = UserCreate(**user_data)
    return user
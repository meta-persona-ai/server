from fastapi_camelcase import CamelModel

class UserUpdate(CamelModel):
    # user_email: str | None = None
    user_name: str | None = None
    user_profile: str | None = None

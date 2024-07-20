import textwrap

class SwaggerConfig:
    def __init__(self):
        self.title = "Persona AI"
        self.version = "0.0.1"
        self.description = textwrap.dedent("""\
            #### 페르소나 AI

            기능 목록:

            * **auth** (_not implemented_).
            * **user** (_not implemented_).
        """)
        self.license_info = {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        }
        self.tags_metadata = [
            {
                "name": "Auth",
                "description": "로그인과 권한 관련 API입니다.",
            },
            {
                "name": "User",
                "description": "유저 관련 API입니다."
            },
            {
                "name": "Chat",
                "description": "채팅방 관련 API입니다."
            },
        ]

    def get_config(self):
        return {
            "title": self.title,
            "version": self.version,
            "description": self.description,
            "license_info": self.license_info,
            "tags_metadata": self.tags_metadata,
        }
from sqlalchemy.orm import Session

from ..schemas import user_schema, schemas
from ..schemas.request import chat_request_schema
from ..crud import auth_crud, user_crud, character_crud, chat_crud

class DatabaseInitializer:
    def __init__(self, engine):
        self.engine = engine
        self.test_email = "test@example.com"
        self.character_name = "init charater"

    def init_db(self):
        db = Session(bind=self.engine)

        self._make_init_user(db)
        self._make_init_character(db)
        self._make_init_chat(db)
        self._make_init_chat(db)

        db.close()

    def _make_init_user(self, db: Session):
        test_user = user_schema.UserCreate(
            user_email=self.test_email,
            user_password="test",
            user_name="Test User",
            user_profile="test.jpg"
        )

        existing_user = user_crud.get_user_by_email(self.test_email, db)
        if not existing_user:
            auth_crud.create_user(test_user, db)

    def _make_init_character(self, db: Session):
        init_user = user_crud.get_user_by_email(self.test_email, db)

        character = schemas.CharacterSchema(
            character_name = self.character_name,
            character_gender = "male",
            character_profile = "init profile",
            character_personality = "init personality",
            character_details = "init details",
            user_id = init_user.user_id
        )

        existing_character = character_crud.get_characters_by_name(self.character_name, db)
        if not existing_character:
            character_crud.create_character(character, db)

    def _make_init_chat(self, db: Session):
        init_user = user_crud.get_user_by_email(self.test_email, db)
        init_character = character_crud.get_characters_by_name(self.character_name, db)

        chat = chat_request_schema.ChatCreate(
            user_id=init_user.user_id,
            character_id=init_character.character_id
        )

        chat_crud.create_chat(chat, db)

import yaml
from sqlalchemy.orm import Session

from ..schemas import user_schema, schemas
from ..schemas.request import chat_request_schema, chat_log_request_schema
from ..crud import auth_crud, user_crud, character_crud, chat_crud, chat_log_crud

class DatabaseInitializer:
    def __init__(self, engine, data_file='example_data.yaml'):
        self.engine = engine
        self.data_file = data_file

    def init_db(self):
        db = Session(bind=self.engine)

        data = self._load_data()
        self._init_users(db, data['users'])
        self._init_characters(db, data['characters'])
        self._init_chats(db, data['chats'])
        self._init_chat_logs(db, data['chat_logs'])

        db.close()

    def _load_data(self):
        with open(self.data_file, 'r') as file:
            return yaml.safe_load(file)

    def _init_users(self, db: Session, users):
        for user_data in users:
            test_user = user_schema.UserCreate(
                user_email=user_data['email'],
                user_password=user_data['password'],
                user_name=user_data['name'],
                user_profile=user_data['profile']
            )

            existing_user = user_crud.get_user_by_email(user_data['email'], db)
            if not existing_user:
                auth_crud.create_user(test_user, db)

    def _init_characters(self, db: Session, characters):
        for char_data in characters:
            init_user = user_crud.get_user_by_email(char_data['user_email'], db)

            character = schemas.CharacterSchema(
                character_name=char_data['name'],
                character_gender=char_data['gender'],
                character_profile=char_data['profile'],
                character_personality=char_data['personality'],
                character_details=char_data['details'],
                user_id=init_user.user_id
            )

            existing_character = character_crud.get_characters_by_name(char_data['name'], db)
            if not existing_character:
                character_crud.create_character(character, db)

    def _init_chats(self, db: Session, chats):
        for chat_data in chats:
            init_user = user_crud.get_user_by_email(chat_data['user_email'], db)
            init_character = character_crud.get_characters_by_name(chat_data['character_name'], db)

            chat = chat_request_schema.ChatCreate(
                user_id=init_user.user_id,
                character_id=init_character.character_id
            )

            chat_crud.create_chat(chat, db)

    def _init_chat_logs(self, db: Session, chat_logs):
        for log_data in chat_logs:
            init_user = user_crud.get_user_by_email(log_data['user_email'], db)
            init_character = character_crud.get_characters_by_name(log_data['character_name'], db)
            init_chat = chat_crud.get_chats_by_user_id(init_user.user_id, db)[0]

            chat_log = chat_log_request_schema.ChatLogCreate(
                chat_id=init_chat.chat_id,
                user_id=init_user.user_id,
                character_id=init_character.character_id,
                role=log_data['role'],
                contents=log_data['contents']
            )

            chat_log_crud.create_chat_log(chat_log, db)

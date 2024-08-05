import yaml
from sqlalchemy.orm import Session

from ..core import settings, setup_logger
from ..schemas.request import (
    chat_request_schema, 
    chat_log_request_schema, 
    user_request_schema, 
    relationship_request_schema, 
    character_request_schema, 
    default_image_request_schema
)
from ..crud import auth_crud, user_crud, character_crud, chat_crud, chat_log_crud, relationship_crud, default_image_crud

logger = setup_logger()

class DatabaseInitializer:
    def __init__(self, engine, data_file='example_data.yaml'):
        self.engine = engine
        self.data_file = data_file

    def init_db(self):
        if settings.drop_table:
            db = Session(bind=self.engine)

            data = self._load_data()

            self._init_users(db, data['users'])
            self._init_relationship(db, data['relationships'])
            self._init_characters(db, data['characters'])
            self._init_chats(db, data['chats'])
            self._init_chat_logs(db, data['chat_logs'])
            self._init_default_images(db, data['default_images'])

            db.close()

            logger.info("📌 Initial data has been successfully inserted into the database.")

    def _load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def _init_users(self, db: Session, users):
        for user_data in users:
            test_user = user_request_schema.UserCreate(
                user_email=user_data['email'],
                user_password=user_data['password'],
                user_name=user_data['name'],
                user_profile=user_data['profile']
            )

            existing_user = user_crud.get_user_by_email(user_data['email'], db)
            if not existing_user:
                auth_crud.create_user(test_user, db)

    def _init_relationship(self, db: Session, relationships):
        for relationship_data in relationships:
            test_relationship = relationship_request_schema.RelationshipCreate(
                relationship_name=relationship_data["relationship_name"]
            )

            existing_relationship = relationship_crud.get_relationship_by_name(relationship_data['relationship_name'], db)
            if not existing_relationship:
                relationship_crud.create_relationship(test_relationship, db)

    def _init_characters(self, db: Session, characters):
        for char_data in characters:
            init_user = user_crud.get_user_by_email(char_data['user_email'], db)

            character = character_request_schema.CharacterCreate(
                character_name=char_data['name'],
                character_profile=char_data['profile'],
                character_gender=char_data['gender'],
                character_personality=char_data['personality'],
                character_details=char_data['details'],
                character_is_public=True,
                relationships=[relationship['relationship_id'] for relationship in char_data['relationships']]
            )

            existing_character = character_crud.get_characters_by_name(char_data['name'], db)
            if not existing_character:
                character_crud.create_character(character, init_user.user_id, db)

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

    def _init_default_images(self, db: Session, default_images):
        for default_image in default_images:
            init_image = default_image_request_schema.DefaultImageCreate(
                image_name=default_image["image_name"],
                image_url=default_image["image_url"],
                image_gender = default_image["image_gender"],
                image_age_group = default_image["image_age_group"]
            )

            existing_relationship = default_image_crud.get_default_images_by_name(default_image['image_name'], db)
            if not existing_relationship:
                default_image_crud.create_image(init_image, db)
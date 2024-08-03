from sqlalchemy.orm import Session
import asyncio
from google.api_core.exceptions import InternalServerError, ServiceUnavailable

from app.core import setup_logger
from app.utils.socket_connection_manager import ConnectionManager
from app.schemas.chatting_schema import CharacterMessage

from app.utils.langchain import Gemini
from app.utils import const
from ..models.chats import Chat
from ..schemas.chatting_schema import UserMessage
from ..schemas.bot_schema import UserSchema, CharacterSchema, ChatLogSchema

from ..utils.socket_handler import create_log_message, insert_message


logger = setup_logger()

async def echo_message(
        room: ConnectionManager, 
        gemini: Gemini,
        chat: Chat, 
        user_message: UserMessage, 
        response_id: int, 
        db: Session
        ):

    await insert_message(chat, user_message.type, user_message.message, db)

    user_log_message = create_log_message("User", chat.chat_id, chat.user.user_name, user_message.message)
    logger.info(user_log_message)

    # output = await generate_bot_response(room, gemini, user_message.message, chat.character.character_name, response_id)
    output = await exception_handler(
        generate_bot_response, room, gemini, user_message.message, chat.character.character_name, response_id
    )
    gemini.add_history(user_message.message, output)
    await insert_message(chat, "character", output, db)
    
    user_log_message = create_log_message("Bot", chat.chat_id, chat.user.user_name, output)
    logger.info(user_log_message)
    
async def exception_handler(func, *args, max_retries: int = const.MAX_RETRIES, retry_delay: int = const.RETRY_DELAY):
    response_message = ""
    for attempt in range(max_retries):
        try:
            response_message = await func(*args)
            break
        except InternalServerError as e:
            if attempt < max_retries - 1:
                logger.warning(f"InternalServerError: {e}. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(retry_delay)
            else:
                logger.error(f"InternalServerError: {e}. All {max_retries} attempts failed.")
                response_message = "Sorry, I'm having trouble processing your request right now. Please try again later."
        except ServiceUnavailable as e:
            if attempt < max_retries - 1:
                logger.warning(f"ServiceUnavailable: {e}. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(retry_delay)
            else:
                logger.error(f"ServiceUnavailable: {e}. All {max_retries} attempts failed.")
                response_message = "The service is currently unavailable. Please try again later."
    
    return response_message

async def generate_bot_response(room: ConnectionManager, gemini: Gemini, inputs: str, character_name: str, response_id: int):
    output = ""
    async for char in gemini.astream_yield(inputs):
        output += char
        response = {
                "type": "character",
                "character_name": character_name,
                "response_id": response_id,
                "character": char
            }
        response_data = CharacterMessage(**response).model_dump_json()
        await room.broadcast(response_data)

    return output

def data_converter(chat: Chat) -> tuple[dict[str, object], dict[str, object], list[dict[str, str]]]:
    user = UserSchema.model_validate(chat.user)
    character = CharacterSchema.model_validate(chat.character)
    chat_logs = [ChatLogSchema.model_validate(log) for log in chat.chat_logs]

    user_info = {
        "user_name": user.user_name,
        "user_birthdate": user.user_birthdate,
        "user_gender": user.user_gender
    }

    character_info = {
        "character_name": character.character_name,
        "character_gender": character.character_gender,
        "character_personality": character.character_personality,
        "character_details": character.character_details,
        "relation_type": ", ".join([c.relationship.relationship_name for c in character.character_relationships])
    }

    chat_history = [{"role": log.role, "content": log.contents} for log in chat_logs]

    return user_info, character_info, chat_history
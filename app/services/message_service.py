from sqlalchemy.orm import Session
import asyncio

from app.core.logger_config import setup_logger
from app.utils.socket_connection_manager import ConnectionManager
from app.schemas.request.chat_log_request_schema import ChatLogCreate
from app.schemas.chatting_schema import CharacterMessage
from app.schemas.schemas import CharacterSchema
from app.services import chat_log_service

logger = setup_logger()

async def echo_message(room: ConnectionManager, chat_log: ChatLogCreate, character_schema: CharacterSchema, response_id: int, db: Session):
    """
    사용자 메시지를 처리하고 봇의 응답을 생성 및 방송합니다.

    Args:
        room (ConnectionManager): 연결된 클라이언트 관리 객체.
        chat_log (ChatLogCreate): 채팅 로그 데이터 객체.
        character_schema (CharacterSchema): 캐릭터 스키마 객체.
        response_id (int): 응답 ID.
        db (Session): 데이터베이스 세션 객체.
    """
    logger.info(f"▶️  User message received: chat_id: {chat_log.chat_id}, user_id: {chat_log.user_id}, contents: {chat_log.contents}")
    
    await insert_user_message(chat_log, db)
    response_message = await generate_bot_response(room, chat_log, character_schema, response_id)
    await insert_bot_message(chat_log, response_message, db)
    
    logger.info(f"▶️  Bot response sent: chat_id: {chat_log.chat_id}, user_id: {chat_log.user_id}, response_message: {response_message}")

async def insert_user_message(chat_log: ChatLogCreate, db: Session):
    """
    사용자 메시지를 데이터베이스에 저장합니다.

    Args:
        chat_log (ChatLogCreate): 채팅 로그 데이터 객체.
        db (Session): 데이터베이스 세션 객체.
    """
    chat_log_service.create_chat_log(chat_log, db)

async def generate_bot_response(room: ConnectionManager, chat_log: ChatLogCreate, character_schema: CharacterSchema, response_id: int):
    """
    봇의 응답 메시지를 생성하고 클라이언트에 방송합니다.

    Args:
        room (ConnectionManager): 연결된 클라이언트 관리 객체.
        chat_log (ChatLogCreate): 채팅 로그 데이터 객체.
        character_schema (CharacterSchema): 캐릭터 스키마 객체.
        response_id (int): 응답 ID.

    Returns:
        str: 생성된 봇 응답 메시지.
    """
    response_message = ""
    for char in chat_log.contents + " response":
        response = {
            "type": "character",
            "character_name": character_schema.character_name,
            "response_id": response_id,
            "character": char
        }
        response_data = CharacterMessage(**response).model_dump_json()
        await room.broadcast(response_data)
        response_message += char
        await asyncio.sleep(0.1)
    return response_message

async def insert_bot_message(chat_log: ChatLogCreate, response_message: str, db: Session):
    """
    봇의 응답 메시지를 데이터베이스에 저장합니다.

    Args:
        chat_log (ChatLogCreate): 채팅 로그 데이터 객체.
        response_message (str): 생성된 봇 응답 메시지.
        db (Session): 데이터베이스 세션 객체.
    """
    chat_log.role = "character"
    chat_log.contents = response_message
    chat_log_service.create_chat_log(chat_log, db)

async def log_insert_data(chat_id: int, user_id: int, character_id: int, role: str, contents: str) -> ChatLogCreate:
    """
    로그 데이터를 생성합니다.

    Args:
        chat_id (int): 채팅 ID.
        user_id (int): 사용자 ID.
        character_id (int): 캐릭터 ID.
        role (str): 메시지의 역할 (사용자 또는 캐릭터).
        contents (str): 메시지 내용.

    Returns:
        ChatLogCreate: 생성된 채팅 로그 데이터 객체.
    """
    return ChatLogCreate(
        chat_id=chat_id,
        user_id=user_id,
        character_id=character_id,
        role=role,
        contents=contents
    )

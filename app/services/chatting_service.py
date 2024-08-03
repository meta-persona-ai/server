from fastapi import WebSocket, HTTPException
from starlette.websockets import WebSocketDisconnect
from sqlalchemy.orm import Session
import asyncio
import json

from app.core import setup_logger
from app.models.users import User
from app.utils.socket_connection_manager import ConnectionManager
from app.utils.socket_room_manager import RoomManager
from ..schemas.chatting_schema import UserMessage
from ..schemas.schemas import CharacterSchema
from ..models.chats import Chat
from ..schemas.bot_schema import UserSchema, CharacterSchema, ChatLogSchema
from ..services.message_service import echo_message
from app.utils.langchain import Gemini

from ..utils.socket_handler import authenticate_user, validate_chat_room, handle_disconnect, handle_exception

logger = setup_logger()
room_manager = RoomManager()

async def chatting(websocket: WebSocket, chat_id: int, db: Session):
    """
    WebSocket 연결을 관리하고 채팅 메시지를 처리하는 함수

    Args:
        websocket (WebSocket): WebSocket 객체.
        chat_id (int): 채팅 방 ID.
        db (Session): 데이터베이스 세션 객체.
    """
    room = room_manager.get_room(chat_id)
    await room.connect(websocket)
    logger.info(f"📌 WebSocket connection established with room: {chat_id}")

    try:
        user: User = await authenticate_user(websocket, db)
        chat = await validate_chat_room(chat_id, user, db)
    except HTTPException as e:
        logger.info(f"❌ {e.detail}")
        await websocket.close(code=1008, reason=e.detail)
        return
    
    logger.info(f"📌 User {user.user_name}({user.user_id}) joined the room {chat_id}")
    await room.broadcast_system_message(f"A new client has joined {chat_id}.")
    
    try:
        await handle_messages(websocket, room, chat, db)
    except WebSocketDisconnect:
        await handle_disconnect(websocket, room_manager, room, chat_id, user)
    except Exception as e:
        await handle_exception(websocket, e)

async def handle_messages(websocket: WebSocket, room: ConnectionManager, chat: Chat, db: Session):
    """
    WebSocket을 통해 수신된 메시지를 처리하고 응답을 생성하는 함수

    Args:
        websocket (WebSocket): WebSocket 객체.
        room (ConnectionManager): 연결된 클라이언트 관리 객체.
        chat_id (int): 채팅 방 ID.
        user (User): 사용자 객체.
        character_schema (CharacterSchema): 캐릭터 스키마 객체.
        db (Session): 데이터베이스 세션 객체.
    """
    user_info, character_info, chat_history = data_converter(chat)

    gemini = Gemini(
        user_info = user_info,
        character_info = character_info, 
        chat_history = chat_history
    )

    while True:
        data = await websocket.receive_text()
        user_message = UserMessage(**json.loads(data))

        response_id = room.get_next_response_id()
        asyncio.create_task(echo_message(room, gemini,chat, user_message, response_id, db=db))

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
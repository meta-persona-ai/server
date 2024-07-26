from fastapi import WebSocket, HTTPException
from starlette.websockets import WebSocketDisconnect
from sqlalchemy.orm import Session
import asyncio
import json

from app.core.logger_config import setup_logger
from app.models.user import User
from app.utils.socket_connection_manager import ConnectionManager
from app.utils.socket_room_manager import RoomManager
from app.utils.jwt_util import verify_token
from app.schemas.chatting_schema import AuthMessage, UserMessage
from app.schemas.schemas import CharacterSchema
from app.services import chat_service, user_service
from app.services.message_service import echo_message, log_insert_data

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
        character_schema = CharacterSchema.model_validate(chat.character)
    except HTTPException as e:
        logger.info(f"❌ {e.detail}")
        await websocket.close(code=1008, reason=e.detail)
        return
    
    logger.info(f"📌 User {user.user_name}({user.user_id}) joined the room {chat_id}")
    await room.broadcast_system_message(f"A new client has joined {chat_id}.")
    
    try:
        await handle_messages(websocket, room, chat_id, user, character_schema, db)
    except WebSocketDisconnect:
        await handle_disconnect(websocket, room, chat_id, user)
    except Exception as e:
        await handle_exception(websocket, e)

async def authenticate_user(websocket: WebSocket, db: Session) -> User:
    """
    WebSocket을 통해 인증 메시지를 수신하고 사용자를 인증하는 함수

    Args:
        websocket (WebSocket): WebSocket 객체.
        db (Session): 데이터베이스 세션 객체.

    Returns:
        User: 인증된 사용자 객체.

    Raises:
        HTTPException: 인증 실패 시 예외 발생.
    """
    auth_message = await websocket.receive_text()
    auth_data = AuthMessage(**json.loads(auth_message))

    if auth_data.type != "auth" or not auth_data.token:
        raise HTTPException(status_code=1008, detail="Authentication failed: Invalid authentication type or missing token")
    
    try:
        user_id = verify_token(auth_data.token).id
        user = user_service.get_user_by_id(user_id, db=db)
        return user
    except HTTPException as e:
        raise HTTPException(status_code=1008, detail=f"Token validation failed: {e.detail}")

async def validate_chat_room(chat_id: int, user: User, db: Session):
    """
    사용자가 특정 채팅 방에 참여할 수 있는지 검증하는 함수

    Args:
        chat_id (int): 채팅 방 ID.
        user (User): 사용자 객체.
        db (Session): 데이터베이스 세션 객체.

    Returns:
        Chat: 채팅 방 객체.

    Raises:
        HTTPException: 사용자가 채팅 방에 참여할 수 없는 경우 예외 발생.
    """
    chat = chat_service.get_chat_by_chat_id_and_user_id(chat_id, user.user_id, db)
    if not chat:
        raise HTTPException(status_code=1008, detail=f"Chat room validation failed: User ({user.user_name}) {user.user_name} is not authorized to join room {chat_id}")
    return chat

async def handle_messages(websocket: WebSocket, room: ConnectionManager, chat_id: int, user: User, character_schema: CharacterSchema, db: Session):
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
    while True:
        data = await websocket.receive_text()
        user_message = UserMessage(**json.loads(data))
        chat_log = await log_insert_data(chat_id, user.user_id, character_schema.character_id, rool=user_message.type, contents=user_message.message)
        response_id = room.get_next_response_id()
        asyncio.create_task(echo_message(room, chat_log, character_schema, response_id, db=db))

async def handle_disconnect(websocket: WebSocket, room: ConnectionManager, chat_id: int, user: User):
    """
    WebSocket 연결이 끊어졌을 때 처리하는 함수

    Args:
        websocket (WebSocket): WebSocket 객체.
        room (ConnectionManager): 연결된 클라이언트 관리 객체.
        chat_id (int): 채팅 방 ID.
        user (User): 사용자 객체.
    """
    room.disconnect(websocket)
    logger.info(f"📌 User {user.user_name}({user.user_id}) disconnected from room {chat_id}")
    await room.broadcast_system_message(f"A client disconnected from {chat_id}.")
    room_manager.cleanup_room(chat_id)

async def handle_exception(websocket: WebSocket, exception: Exception):
    """
    예외 발생 시 WebSocket 연결을 종료하는 함수

    Args:
        websocket (WebSocket): WebSocket 객체.
        exception (Exception): 발생한 예외.
    """
    logger.error(f"❌ An error occurred: {exception}")
    await websocket.close(code=1011)  # Internal Server Error

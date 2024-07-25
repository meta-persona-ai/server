from fastapi import WebSocket, HTTPException
from starlette.websockets import WebSocketDisconnect
from sqlalchemy.orm import Session
import asyncio
import json

from app.core.logger_config import setup_logger
from app.utils.socket_connection_manager import ConnectionManager
from app.utils.socket_room_manager import RoomManager
from app.utils.jwt_util import verify_token
from app.services import chat_service
from app.schemas.chatting_schema import AuthMessage, UserMessage, CharacterMessage
from app.schemas.schemas import CharacterSchema


logger = setup_logger()
room_manager = RoomManager()


async def echo_message(room: ConnectionManager, data: UserMessage, character_schema: CharacterSchema, response_id: int):
    for char in data.message:
        response = {
            "type": "character",
            "character_name": character_schema.character_name,
            "response_id": 1,
            "character": char
        }
        response_data = CharacterMessage(**response).model_dump_json()
        await room.broadcast(response_data)
        await asyncio.sleep(0.1)


async def chatting(websocket: WebSocket, room_name: int, db: Session):
    room = room_manager.get_room(room_name)
    await room.connect(websocket)
    logger.info(f"📌 WebSocket connection established with room: {room_name}")

    # Get Token
    auth_message = await websocket.receive_text()
    auth_data = AuthMessage(**json.loads(auth_message))

    # Token Verification
    if auth_data.type != "auth" or not auth_data.token:
        logger.info("❌ Authentication failed: Invalid authentication type or missing token")
        await websocket.close(code=1008)
        return
    
    # Token Validation
    try:
        user = verify_token(auth_data.token)
        logger.info(f"✅ Token validation successful for user: ({user.id}) {user.name}")
    except HTTPException as e:
        logger.info(f"❌ Token validation failed: {e.detail}")
        await websocket.close(code=1008)
        return
    
    # Chat Room Validation
    chat = chat_service.get_chats_by_chat_id_and_user_id(room_name, user.id, db)
    character_schema = CharacterSchema.model_validate(chat.character)
    
    if not chat:
        logger.info(f"❌ Chat room validation failed: User ({user.id}) {user.name} is not authorized to join room {room_name}")
        await websocket.close(code=1008)
        return

    # Chatting Start
    logger.info(f"📌 User ({user.id}) {user.name} joined the room {room_name}")
    try:
        await room.broadcast_system_message(f"A new client has joined {room_name}.")
        while True:
            data = await websocket.receive_text()
            user_message = UserMessage(**json.loads(data))
            response_id = room.get_next_response_id()
            asyncio.create_task(echo_message(room, user_message, character_schema, response_id))
    except WebSocketDisconnect:
        room.disconnect(websocket)
        logger.info(f"📌 User ({user.id}) {user.name} disconnected from room {room_name}")
        await room.broadcast_system_message(f"A client disconnected from {room_name}.")
        room_manager.cleanup_room(room_name)
    except RuntimeError as e:
        logger.error(f"❌ An error occurred during runtime: {e}")
        await websocket.close(code=1011)  # Internal Server Error
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        await websocket.close(code=1011)  # Internal Server Error
        
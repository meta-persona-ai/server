from fastapi import WebSocket, HTTPException
from starlette.websockets import WebSocketDisconnect
from datetime import datetime
import asyncio
import json

from app.core.logger_config import setup_logger
from app.utils.socket_connection_manager import ConnectionManager
from app.utils.socket_room_manager import RoomManager
from app.utils.jwt_util import verify_token


logger = setup_logger()
room_manager = RoomManager()


async def echo_message(websocket: WebSocket, data: str, response_id: int):
    for char in data:
        json_message = json.dumps({"response_id": response_id, "character": char})
        await websocket.send_text(json_message)
        await asyncio.sleep(1)

async def echo_message2(room: ConnectionManager, data: str, response_id: int):
    for char in data:
        json_message = json.dumps({"response_id": response_id, "character": char})
        await room.broadcast(json_message)
        await asyncio.sleep(0.1)

async def send_time(websocket: WebSocket):
    while True:
        await asyncio.sleep(5)
        json_message = json.dumps({"time": datetime.utcnow().isoformat()})
        await websocket.send_text(json_message)


async def chatting(websocket: WebSocket, room_name: int):
    room = room_manager.get_room(room_name)
    await room.connect(websocket)
    logger.info(f"📌 WebSocket connection established with room: {room_name}")

    # Get Token
    auth_message = await websocket.receive_text()
    auth_data = json.loads(auth_message)

    # Token Verification
    if auth_data.get("type") != "auth" or not auth_data.get("token"):
        logger.info("❌ Authentication failed: Invalid authentication type or missing token")
        await websocket.close(code=1008)
        return
    
    # Token Validation
    try:
        user = verify_token(auth_data["token"])
        logger.info(f"✅ Token validation successful for user: ({user.id}) {user.name}")
    except HTTPException as e:
        logger.info(f"❌ Token validation failed: {e.detail}")
        await websocket.close(code=1008)
        return
    
    # Chat Room Validation
    

    # Chatting Start
    logger.info(f"📌 User ({user.id}) {user.name} joined the room {room_name}")
    await room.broadcast(json.dumps({"message": f"A new client has joined {room_name}."}))
    try:
        while True:
            data = await websocket.receive_text()
            response_id = room.get_next_response_id()
            asyncio.create_task(echo_message2(room, data, response_id))
    except WebSocketDisconnect:
        room.disconnect(websocket)
        logger.info(f"📌 User ({user.id}) {user.name} disconnected from room {room_name}")
        await room.broadcast(f"A client disconnected from {room_name}.")
        room_manager.cleanup_room(room_name)
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        
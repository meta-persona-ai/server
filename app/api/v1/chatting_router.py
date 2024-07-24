from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.security import APIKeyHeader
from starlette.websockets import WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os
import asyncio
import json

from app.utils.socket_room_manager import RoomManager
from app.utils.socket_connection_manager import ConnectionManager
from app.services import chat_log_service


router = APIRouter(
    prefix="/api/chatting",
    tags=["Chatting"]
)
api_key_header = APIKeyHeader(name="Authorization")
room_manager = RoomManager()


@router.get("/", response_class=HTMLResponse)
async def serve_homepage():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    file_path = os.path.join(project_root, "app", "templates", "chatting.html")
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@router.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    room = room_manager.get_room(room_name)
    await room.connect(websocket)

    await room.broadcast(json.dumps({"message": f"A new client has joined {room_name}."}))
    try:
        while True:
            data = await websocket.receive_text()
            response_id = room.get_next_response_id()
            asyncio.create_task(chat_log_service.echo_message2(room, data, response_id))
    except WebSocketDisconnect:
        room.disconnect(websocket)
        await room.broadcast(f"A client disconnected from {room_name}.")
        room_manager.cleanup_room(room_name)
    except Exception as e:
        print(f"An error occurred: {e}")
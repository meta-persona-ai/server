from fastapi import APIRouter, WebSocket
from fastapi.security import APIKeyHeader
from fastapi.responses import HTMLResponse
import os

from app.services import chatting_service


router = APIRouter(
    prefix="/api/chatting",
    tags=["Chatting"]
)
api_key_header = APIKeyHeader(name="Authorization")


@router.get("/", response_class=HTMLResponse)
async def serve_homepage():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    file_path = os.path.join(project_root, "app", "templates", "chatting.html")
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@router.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    await chatting_service.chatting(websocket, room_name)

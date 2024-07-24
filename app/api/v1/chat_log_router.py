from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyHeader
from starlette.websockets import WebSocketDisconnect
import os
import asyncio

from app.services import chat_log_service


router = APIRouter(
    prefix="/api/chat-log",
    tags=["Chat log"]
)
api_key_header = APIKeyHeader(name="Authorization")

@router.get("/", response_class=HTMLResponse)
async def serve_homepage():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    file_path = os.path.join(project_root, "app", "templates", "client.html")
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)




@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    response_id = 0  # Initialize response ID
    try:
        while True:
            data = await websocket.receive_text()
            response_id += 1
            asyncio.create_task(chat_log_service.echo_message(websocket, data, response_id))
    except WebSocketDisconnect:
        print("WebSocketDisconnect!!")

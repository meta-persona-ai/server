from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyHeader
from starlette.websockets import WebSocketDisconnect
import os
import asyncio
from datetime import datetime
import json

router = APIRouter(
    prefix="/api/chatting",
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



async def echo_message(websocket: WebSocket, data: str, response_id: int):
    for char in data:
        json_message = json.dumps({"response_id": response_id, "character": char})
        await websocket.send_text(json_message)
        await asyncio.sleep(1)

async def send_time(websocket: WebSocket):
    while True:
        await asyncio.sleep(5)
        json_message = json.dumps({"time": datetime.utcnow().isoformat()})
        await websocket.send_text(json_message)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    send_time_task = asyncio.create_task(send_time(websocket))
    response_id = 0  # Initialize response ID
    try:
        while True:
            data = await websocket.receive_text()
            response_id += 1
            asyncio.create_task(echo_message(websocket, data, response_id))
    except WebSocketDisconnect:
        print("WebSocketDisconnect!!")
    finally:
        send_time_task.cancel()  # WebSocket 연결이 끊어지면 send_time_task를 취소
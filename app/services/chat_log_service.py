from fastapi import WebSocket
import asyncio
from datetime import datetime
import json

from app.utils.socket_connection_manager import ConnectionManager


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

from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyHeader
from starlette.websockets import WebSocketDisconnect
import os
import asyncio

from app.services import chat_log_service


router = APIRouter(
    prefix="/api/v1/chat-log",
    tags=["Chat log"]
)
api_key_header = APIKeyHeader(name="Authorization")


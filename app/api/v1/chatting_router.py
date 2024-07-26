from fastapi import APIRouter, WebSocket, Depends
from fastapi.security import APIKeyHeader
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os

from app.db.database import get_db
from app.services import chatting_service


router = APIRouter(
    prefix="/api/v1/chatting",
    tags=["Chatting"]
)
api_key_header = APIKeyHeader(name="Authorization")


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, db: Session = Depends(get_db)):
    await chatting_service.chatting(websocket, chat_id, db)

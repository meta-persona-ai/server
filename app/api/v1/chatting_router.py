from fastapi import APIRouter, WebSocket, Depends
from fastapi.security import APIKeyHeader
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os

from app.db.database import get_db
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


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, db: Session = Depends(get_db)):
    await chatting_service.chatting(websocket, chat_id, db)

from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...services import chatting_service

router = APIRouter(
    prefix="/api/v1/chatting",
    tags=["Chatting"]
)

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, db: Session = Depends(get_db)):
    await chatting_service.chatting(websocket, chat_id, db)

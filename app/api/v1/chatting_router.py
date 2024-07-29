from fastapi import APIRouter, WebSocket, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

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


from app.utils.langchain import GeminiChain, simple_chat

@router.get("/test")
async def chatbot():
    chain = GeminiChain()

    # astream 메서드 호출
    input_text = "python에 대해 3줄로 알려줄래?"
    output = await chain.astream(input_text)

    content = {"result": output}
    # print(content)
    # return JSONResponse(content=content, media_type="application/json; charset=utf-8")


@router.get("/simple_test")
async def simple():
    output = await simple_chat("python")

    content = {"result": output}
    print(content)
    # Response(content=json.dumps(content), media_type="application/json; charset=utf-8")
    # return JSONResponse(content=content, media_type="application/json; charset=utf-8")

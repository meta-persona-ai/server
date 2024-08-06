from fastapi import WebSocket, HTTPException
from starlette.websockets import WebSocketDisconnect

from ..core import setup_logger
from ..utils.socket_connection_manager import ConnectionManager
from ..utils.socket_room_manager import RoomManager
from ..models import User

from ..utils.socket_handler import authenticate_user, validate_chat_room, handle_disconnect, handle_exception

logger = setup_logger()

async def handle_websocket_exceptions(websocket: WebSocket, room_manager: RoomManager, room: ConnectionManager, chat_id: int, user: User, callback):
    """
    WebSocket 연결과 관련된 예외를 처리하는 함수

    Args:
        websocket (WebSocket): WebSocket 객체.
        room_manager (RoomManager): 룸 관리 객체.
        room (ConnectionManager): 연결된 클라이언트 관리 객체.
        chat_id (int): 채팅 방 ID.
        user (User): 사용자 객체.
        callback (Callable): WebSocket 핸들러 콜백 함수.
    """
    try:
        await callback()
    except HTTPException as e:
        logger.info(f"❌ {e.detail}")
        await websocket.close(code=1008, reason=e.detail)
    except RuntimeError:
        logger.warning(f"Failed to send message to connection - room: {chat_id}")
        await websocket.close(code=1008, reason="Failed to broadcast system message.")
    except WebSocketDisconnect:
        await handle_disconnect(websocket, room_manager, room, chat_id, user)
    except Exception as e:
        await handle_exception(websocket, e)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.relationship_service import RelationshipService
from app.schemas.request.relationship_request_schema import RelationshipCreate, RelationshipUpdate
from app.schemas.response.relationship_response_schema import RelationshipResponse, MessageResponse

router = APIRouter(
    prefix="/api/v1/relationship",
    tags=["Relationship"]
)

@router.post("/",
            description="새 관계를 생성하는 API입니다.",
            response_model=MessageResponse
            )
async def create_relationship(relationship: RelationshipCreate, db: Session = Depends(get_db)):
    relationship = RelationshipService.create_relationship(relationship, db=db)
    return {"message": "Relationship created successfully"} if relationship else {"message": "Relationship creation failed"}

@router.get("/",
            description="모든 관계를 조회하는 API입니다.",
            response_model=list[RelationshipResponse]
            )
async def get_relationships(db: Session = Depends(get_db)):
    return RelationshipService.get_relationships(db)

@router.put("/{relationship_id}",
               description="관계를 수정하는 API입니다.",
               response_model=MessageResponse
               )
async def update_relationship(relationship_id: int, relationship: RelationshipUpdate, db: Session = Depends(get_db)):
    relationship = RelationshipService.update_relationship(relationship_id, relationship, db)
    return {"message": "Relationship updated successfully"} if relationship else {"message": "Relationship updated failed"}

@router.delete("/{relationship_id}",
               description="관계를 삭제하는 API입니다.",
               response_model=MessageResponse
               )
async def delete_relationship(relationship_id: int, db: Session = Depends(get_db)):
    relationship = RelationshipService.delete_relationship(relationship_id, db)
    return {"message": "Relationship deleted successfully"} if relationship else {"message": "Relationship deletion failed"}

# @router.delete("/{chat_id}",
#                description="관계를 삭제하는 API입니다.",
#                response_model=MessageResponse
#                )
# async def delete_chat(chat_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
#     success = chat_service.delete_chat_by_id(chat_id, user_id, db)
#     return {"message": "Chat deleted successfully"} if success else {"message": "Chat deletion failed"}

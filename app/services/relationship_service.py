from sqlalchemy.orm import Session
from app.crud import relationship_crud
from ..schemas.request.relationship_request_schema import RelationshipCreate, RelationshipUpdate

class RelationshipService:
    @staticmethod
    def create_relationship(relationship: RelationshipCreate, db: Session):
        return relationship_crud.create_relationship(relationship, db)

    @staticmethod
    def get_relationships(db: Session):
        return relationship_crud.get_relationships(db)

    @staticmethod
    def get_relationship_by_id(relationship_id: int, db: Session):
        return relationship_crud.get_relationship_by_id(relationship_id, db)

    @staticmethod
    def update_relationship(relationship_id: int, relationship_update: RelationshipUpdate, db: Session):
        return relationship_crud.update_relationship(relationship_id, relationship_update, db)

    @staticmethod
    def delete_relationship(relationship_id: int, db: Session):
        return relationship_crud.delete_relationship(relationship_id, db)

from sqlalchemy.orm import Session
from ..models.relationship import Relationship
from ..schemas.request.relationship_request_schema import RelationshipCreate, RelationshipUpdate


# Create
def create_relationship(relationship: RelationshipCreate, db: Session):
    db_relationship = Relationship(
        relationship_name=relationship.relationship_name
    )
    db.add(db_relationship)
    db.commit()
    db.refresh(db_relationship)
    return db_relationship

# Read
def get_relationships(db: Session) -> list[Relationship]:
    return db.query(Relationship).all()

def get_relationship_by_id(relationship_id: int, db: Session) -> Relationship:
    return db.query(Relationship).filter(Relationship.relationship_id == relationship_id).first()

def get_relationship_by_name(relationship_name: str, db: Session) -> Relationship:
    return db.query(Relationship).filter(Relationship.relationship_name == relationship_name).first()

# Update
def update_relationship(relationship_id: int, relationship_update: RelationshipUpdate, db: Session):
    db_relationship = get_relationship_by_id(relationship_id, db)
    if db_relationship:
        db_relationship.relationship_name = relationship_update.relationship_name
        db.commit()
        db.refresh(db_relationship)
        return db_relationship
    return None

# Delete
def delete_relationship(relationship_id: int, db: Session) -> bool:
    db_relationship = get_relationship_by_id(relationship_id, db)
    if db_relationship:
        db.delete(db_relationship)
        db.commit()
        return True
    return False

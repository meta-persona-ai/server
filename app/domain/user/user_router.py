from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.user.user_response_schema import User
from . import user_service


router = APIRouter(
    prefix="/api/user",
    tags=["User"]
)


@router.get("/all",
            description="모든 유저를 조회합니다.",
            response_model=list[User]
            )
async def read_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.get("/id/{user_id}",
            description="유저 ID로 유저를 조회합니다.",
            response_model=User
            )
async def read_users_by_id(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(user_id, db)

@router.get("/email/{user_email}",
            description="유저 이메일로 유저를 조회합니다.",
            response_model=User
            )
async def read_users_by_id(user_email: str, db: Session = Depends(get_db)):
    return user_service.get_user_by_email(user_email, db)

@router.delete("/users/{user_id}",
               description="유저 ID로 유저를 삭제합니다.",
               response_model=dict
               )
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = user_service.delete_user_by_id(user_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# @router.post("/users/", response_model=user_response_schema.User)
# def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     created_user = user_crud.create_user(db=db, user=user)
#     return created_user


# @router.get("/users/", response_model=list[user_response_schema.User])
# def read_users(db: Session = Depends(get_db)):
#     users = user_crud.get_users(db)
#     return users


# @router.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @router.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @router.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
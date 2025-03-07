from fastapi import APIRouter
from pydantic import BaseModel

from modules.db import models
from modules.db.db_manager import db


router = APIRouter()


class User(BaseModel):
    user_id: int
    chat_id: str
    phone: str
    name: str
    last_name: str
    
@router.get('/api/v1/users', tags=['user'], response_model=list[User])
async def get_users():
    with db.create_session() as session:
        return session.query(models.User).all()

@router.get('/api/v1/users/{user_id}', tags=['user'], response_model=User)
async def get_user(user_id: int):
    with db.create_session() as session:
        return session.query(models.User).filter_by(product_id=user_id).first()
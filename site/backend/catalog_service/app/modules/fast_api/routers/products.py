from fastapi import APIRouter
from pydantic import BaseModel

from modules.db import models
from modules.db.db_manager import db


router = APIRouter()


class Product(BaseModel):
    product_id: int
    name: str
    description: str
    price: float
    image: str
    
    
@router.get('/api/v1/catalog/products', tags=['products'], response_model=list[Product])
async def get_products():
    with db.create_session() as session:
        return session.query(models.Product).all()

@router.get('/api/v1/catalog/{product_id}', tags=['products'], response_model=Product)
async def get_product(product_id: int):
    with db.create_session() as session:
        return session.query(models.Product).filter_by(product_id=product_id).first()
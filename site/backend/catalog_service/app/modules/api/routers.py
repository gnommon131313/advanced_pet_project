import requests, os
from io import BytesIO
from fastapi import APIRouter
from pydantic import BaseModel

from modules.db import models
from modules.db.db_manager import db
from modules.utils.s3_client import s3_client


router = APIRouter()


class Product(BaseModel):
    product_id: int
    name: str
    description: str
    price: float
    image: str
    
    
@router.get('/api/v1/catalog', tags=['catalog'], response_model=list[Product])
async def get_products():
    with db.create_session() as session:
        products = session.query(models.Product).all()
        
        for product in products:
            product.image = await s3_client.create_presigned_url(
                bucket_name=os.getenv('MINIO_BUCKET_NAME'),
                object_name=product.image, 
                expiration=60
            )  

        return products

@router.get('/api/v1/catalog/{product_id}', tags=['catalog'], response_model=Product)
async def get_product(product_id: int):
    with db.create_session() as session:
        return session.query(models.Product).filter_by(product_id=product_id).first()
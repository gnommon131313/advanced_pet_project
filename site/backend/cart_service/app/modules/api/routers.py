from fastapi import APIRouter, FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

from modules.db import models
from modules.db.db_manager import db


router = APIRouter()


class Cart(BaseModel):
    cart_id: int
    user_chat_id: int  # при необходимости само расширеться до BigInteger, в отличии от моделей sqlalchemy
    
    
class CartProducts(BaseModel):
    cart_id: int
    product_id: int
    quantity: int
    total: int
    
    
class PostData(BaseModel):
    product_id : int = Field(alias='productId') # важно, чтобы названия полей в JSON запросе совпадали с названиями атрибутов в pydantic модели. Можно просто назвать поля и атрибуты одинаково, но т.к. в JS и Python приняты разные именования полей тут это будет не сооответствовать стандарту и лучше использовать связывание с полем через `int = Field(alias='НАЗЫВАНИЕ ПОЛЮ В JSON ЗАПРОСЕ')` 
    
    
@router.get('/api/v1/carts/{user_chat_id}', tags=['cart'], response_model=CartProducts)
async def get_cart_products(user_chat_id: int):
    with db.create_session() as session:
        cart = session.query(models.Cart).filter_by(user_chat_id=user_chat_id).first()
        
        return session.query(models.CartProduct).filter_by(cart_id=cart.cart_id).first()
    
@router.post("/api/v1/carts/{user_chat_id}")
async def create_product_in_cart(user_chat_id: int, post_data: PostData):
    with db.create_session() as session:
        print(f'\nЗапрос на добавление продукта для: {user_chat_id} {post_data.product_id}\n')
        
        # cart = session.query(models.Cart).filter_by(user_chat_id=user_chat_id).first()
        
        # if (cart == None):
        #     raise HTTPException(status_code=404, detail=f'ERR: не удалось найти Cart для данного user_chat_id={user_chat_id}')

        # product = session.query(models.CartProduct).filter_by(cart_id=cart.id, product_id=cart_data.product_id).first()
        
        # # Увеличить количество
        # if(product):
        #     product.quantity += 1
            
        # else:
        #     product = models.CartProduct(cart_id=cart.id, product_id=cart_data.product_id, quantity=1)
        #     session.add(product)
            
        # # Запрос к калатогу товаров
        # async with httpx.AsyncClient() as client:
        #     response = await client.get('http://localhost/api/catalog/products')
        
        #     if response.status_code != 200:
        #         raise HTTPException(status_code=response.status_code, detail="Error fetching data")
            
        #     # Расчитать цену
        #     data = json.loads(response.text)  # Преобразуем строку JSON в объект Python
        #     product.total = product.quantity * float(data[product.product_id - 1]['price'])
            
        # if (product.total == None or product.total == 0):
        #     raise HTTPException(status_code=400, detail="Не удалось расчитать Total Price")
        
        # session.commit()
        
    return {"msg": "response is success"}
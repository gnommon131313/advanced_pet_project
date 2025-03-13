from decimal import Decimal
from datetime import date, datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import  Column, Integer, String, Text, Boolean, TIMESTAMP, Date, ForeignKey, Numeric, CheckConstraint, BigInteger


class Base(DeclarativeBase): 
    pass


class Cart(Base):
    __tablename__ = 'carts'
    
    cart_id: Mapped[int] = Column(Integer(), primary_key=True)
    user_chat_id: Mapped[int] = Column(BigInteger(), nullable=False)


class CartProduct(Base):
    __tablename__ = 'cart_products'
    
    cart_id: Mapped[int] = Column(Integer(), primary_key=True)
    product_id: Mapped[int] = Column(Integer(), primary_key=True, nullable=False)
    quantity: Mapped[int] = Column(Integer(), default=1, nullable=False)
    total: Mapped[int] = Column(Integer(), default=1, nullable=False)
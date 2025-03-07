from decimal import Decimal
from datetime import date, datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import  Column, Integer, String, Text, Boolean, TIMESTAMP, Date, ForeignKey, Numeric, CheckConstraint


class Base(DeclarativeBase): 
    pass


class Product(Base):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text(), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False, default="...")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    image: Mapped[str] = mapped_column(Text(), nullable=False)
    
    # Ограничения можно сразу записать в поле, но рекомендация записывать все огранчиения в одном месте
    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
    )
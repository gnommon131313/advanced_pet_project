from datetime import date, datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import  Column, Integer, String, Text, Boolean, TIMESTAMP, Date, ForeignKey


class Base(DeclarativeBase): 
    pass


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP(), nullable=True)
    chat_id: Mapped[str] = mapped_column(Text(), nullable=True)
    user_chat_id: Mapped[str] = mapped_column(Text(), nullable=True)
    text: Mapped[str] = mapped_column(Text(), nullable=True)
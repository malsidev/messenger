from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, NotNullable, Uuid,TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str| None] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String())
    is_active: Mapped[Boolean] = mapped_column(Boolean, default=True)

class Chats(Base):
    __tablename__ = 'chats'

    id : Mapped[int] = mapped_column(primary_key=True)
    public_id : Mapped[str] = mapped_column(Uuid)
    user1_id: Mapped[int] = mapped_column(Integer)
    user2_id: Mapped[int] = mapped_column(Integer)

    create_at : Mapped[int] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
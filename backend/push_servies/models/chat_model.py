import uuid

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, NotNullable, Uuid,TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base


class Base(DeclarativeBase):
    pass


class Chats(Base):
    __tablename__ = 'chats'

    id : Mapped[int] = mapped_column(primary_key=True)
    public_id : Mapped[str] = mapped_column(Uuid, default=uuid.uuid4)
    user1_id: Mapped[int] = mapped_column(Integer)
    user2_id: Mapped[int] = mapped_column(Integer)

    create_at : Mapped[int] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
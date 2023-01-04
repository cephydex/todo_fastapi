from .database import Base
from sqlalchemy import (
        TIMESTAMP, Column, Boolean, String, Integer, Table, 
        CheckConstraint, ForeignKey
    )
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import List, Optional
# from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

class Todo(Base):
    """Todo, assignable to a user

    Args:
        Base: Base model

    Returns:
        dict: return object format for responses
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # id = Column(GUID, primary_key=True,
    #             server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=True)
    active = Column(Boolean, nullable=False, server_default="True")

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    def __str__(self) -> str:
        return f'{self.id} | {self.title} | {self.content} | {self.active} | {self.created_at}'

user_todo = Table(
    "user_todos",
    Base.metadata,
    Column(
        "user_id", 
        Integer, ForeignKey("users.id"),
        primary_key=True
    ),
    Column(
        "todo_id", 
        Integer, ForeignKey("todos.id"),
        primary_key=True
    )
)

class User(Base):
    """User table model

    Args:
        Base: Base model

    Returns:
        User: User object
    """
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, nullable=True)
    email: str = Column(String(128), unique=True, nullable=False)
    password: str = Column('password', String(100), nullable=False)
    active: bool = Column(Boolean, server_default='True', nullable=False)
    todos = relationship(Todo, secondary=user_todo, backref='user_todos')

    __table_args__ = (
        CheckConstraint('char_length(password) > 8',
            name='password_min_length'),
    )

    def __str__(self) -> str:
        return f'{self.id} | {self.email} | {self.password} | {self.active}'



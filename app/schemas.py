from pydantic import BaseModel
from datetime import datetime
from typing import List


class TodoInsertSchema(BaseModel):
    id: int | None = None
    title: str
    content: str
    category : str | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name: True
        arbitrary_types_allowed = True

class TodoBaseSchema(BaseModel):
    id: int | None = None
    # id: str | None = None
    title: str
    content: str
    category : str | None = None
    active: bool | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name: True
        arbitrary_types_allowed = True

class ListResponse(BaseModel):
    success: str
    message: str
    data: List


class UserSchema(BaseModel):
    id: int | None = None
    email: str
    password: str

    class Config:
        orm_mode = True

from pydantic import BaseModel
from datetime import datetime
from typing import List

class CategoryCreate(BaseModel):
    title: str | None
    description: str | None

class CategoryOut(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime

class CategoryUpdate(BaseModel):
    category_id: int
    new_title: str | None
    new_description: str | None
    owner_username: str
    updated_at: datetime

class CategoryDelete(BaseModel):
    category_id: int
    owner_username: str

class CategoryListResponse(BaseModel):
    items: List[CategoryOut]

from pydantic import BaseModel
from typing import List
from typing import Optional

class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    currency: str
    category_id: Optional[int] = None

class ProductUpdate(BaseModel):
    owner_username: str | None = None
    new_title: str | None
    new_description: str | None = None
    new_price: float | None = None
    new_currency: str | None = None
    new_category_id: int | None = None



class ProductOutput(BaseModel):

    id: int
    title: str
    description: str | None
    category_id: int | None
    price: int
    currency: str

class ProductDelete(BaseModel):
    owner_username: str | None = None

class ProductListResponse(BaseModel):
    items: List[ProductOutput]
    total: int
    page: int
    limit: int
    pages: int

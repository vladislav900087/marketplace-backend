from pydantic import BaseModel
from typing import List

# input model
class CartItemIn(BaseModel):
    product_id: int
    quantity: int = 1

# deletion model
class CartItemDelete(BaseModel):
    owner_username: str
    product_id: int

# cart clearance model
class UserCartClear(BaseModel):
    owner_username: str


class CartItemOut(BaseModel):
    product_id: int
    title: str
    price: int
    quantity: int
    subtotal: int

class CartOut(BaseModel):
    items: List[CartItemOut]
    total_price: int
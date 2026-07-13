from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    total_price: float
    created_at: datetime

class OrderConfirm(BaseModel):
    order_id: int
    action: str

class OrderListResponse(BaseModel):
    items: List[OrderOut]
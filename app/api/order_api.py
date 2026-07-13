# fast api tools
from fastapi import APIRouter, Depends
# db calling
from app.core.database import get_db
from sqlalchemy.orm import Session
# models
from app.models.user_model import User
# services
from app.services.order_service import OrderService
# getting current authorized user
from app.auth.auth import get_current_user, rate_limit
# schemas
from app.schemas.order_schemas import OrderOut, OrderConfirm, OrderListResponse


order_router = APIRouter(prefix='/orders', tags=['Orders'])
order_service = OrderService()


@order_router.post('/add', response_model=OrderOut)
async def create_order(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _: None = Depends(rate_limit)):
    return order_service.create_order(db=db, username=str(current_user.username))

@order_router.post('/confirm', response_model=OrderOut)
async def confirm_order(data: OrderConfirm, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _: None = Depends(rate_limit)):
    return order_service.confirm_order(db=db, username=str(current_user.username), order_id=data.order_id, action=data.action)

@order_router.get('/', response_model=OrderListResponse)
async def get_user_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    return order_service.get_user_orders(db=db, username=str(current_user.username))

@order_router.get('/{order_id}', response_model=OrderOut)
async def get_my_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    return order_service.get_user_order(db=db, username=str(current_user.username), order_id=order_id)


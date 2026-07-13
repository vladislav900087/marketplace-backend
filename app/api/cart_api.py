# fastapi base tools
from fastapi import APIRouter, Depends, HTTPException
# database session data type
from sqlalchemy.orm import Session
# database itself
from app.core.database import get_db
# current authorized user
from app.auth.auth import get_current_user, rate_limit
# cart functionality service
from app.services.cart_service import CartService
# utils
from app.services.utilities import Utilities
# models
from app.models.user_model import User
# pydantic models
from app.schemas.cart_schemas import CartItemIn, CartItemDelete, CartOut, UserCartClear


cart_router = APIRouter(prefix='/cart', tags=['User Cart'])
cart_service = CartService()
utils = Utilities()

@cart_router.post('/add')
async def add_to_cart(data: CartItemIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _: None = Depends(rate_limit)):
    return cart_service.add_to_cart(username=current_user.username, db=db, product_id=data.product_id, quantity=data.quantity)

# route for admins
@cart_router.get('/other')
async def get_other_user_cart(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='You don\'t have admin privileges')

    return cart_service.get_user_cart(username=username, db=db)



@cart_router.get('/items', response_model=CartOut)
async def get_user_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    return cart_service.get_user_cart(username=current_user.username, db=db)

@cart_router.delete('/delete')
async def delete_from_cart(data: CartItemDelete, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _: None = Depends(rate_limit)):
    owner_username = utils.get_user_permissions(current_user=current_user, data=data)
    return cart_service.remove_from_cart(db=db, username=owner_username, product_id=data.product_id)

@cart_router.delete('/clear')
async def clear_cart(data: UserCartClear, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    owner_username = utils.get_user_permissions(current_user=current_user, data=data)
    return cart_service.clear_cart(username=owner_username, db=db)

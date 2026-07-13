# main fastapi tools


from fastapi import APIRouter, Depends, HTTPException, status
# session dt
from sqlalchemy.orm import Session
# services and functions
from app.services.product_service import ProductService
from app.auth.auth import get_current_user, rate_limit
from app.core.database import get_db
# models
from app.models.user_model import User
# schemas
from app.schemas.product_schemas import ProductCreate, ProductUpdate, ProductOutput, ProductDelete
# typing
from typing import List



product_router = APIRouter()
product_service = ProductService()

@product_router.get('/products')
async def get_user_products(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    try:
        return product_service.get_all_products(db=db, owner_username=str(current_user.username))
    except Exception as e:
        product_service.raise_error(e=e)

# admin api route
@product_router.get('/other_products/{username}')
async def get_someone_else_products(username: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have permission')

    return product_service.get_all_products(db=db, owner_username=username)



@product_router.get('/products/{product_id}')
async def get_single_user_product(product_id: int, db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    try:
        return product_service.get_single_product(product_id=product_id, db=db)
    except Exception as e:
        product_service.raise_error(e=e)

@product_router.post('/products', response_model=ProductOutput)
async def create_user_product(data: ProductCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    try:
        return product_service.create_product(db=db, owner_username=str(current_user.username), title=data.title, price=data.price, currency=data.currency, category_id=data.category_id, description=data.description)
    except Exception as e:
        product_service.raise_error(e=e)

# role-based access
@product_router.put('/products/{product_id}')
async def update_user_product(product_id: int, data: ProductUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    try:
        owner_username = product_service.get_user_permissions(current_user_username=str(current_user.username), current_user_role=str(current_user.role), product_data=data)
        return product_service.update_product(db=db, owner_username=owner_username, product_id=product_id, new_title=data.new_title, new_price=data.new_price, new_currency=data.new_currency, new_category_id=data.new_category_id, new_description=data.new_description)
    except Exception as e:
        product_service.raise_error(e=e)

# role-based access
@product_router.delete('/products/{product_id}')
async def delete_user_product(product_id: int, data: ProductDelete, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):

    try:
        owner_username = product_service.get_user_permissions(current_user_username=str(current_user.username), current_user_role=str(current_user.role), product_data=data)
        return product_service.delete_product(product_id=product_id, db=db, owner_username=owner_username)
    except Exception as e:
        product_service.raise_error(e=e)






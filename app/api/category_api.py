from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.auth import get_current_user, rate_limit
from app.services.category_service import CategoryService
from app.services.utilities import Utilities
from app.models.user_model import User
from app.schemas.category_schemas import CategoryCreate, CategoryOut, CategoryUpdate, CategoryDelete, CategoryListResponse


category_router = APIRouter(prefix='/categories', tags=['Categories'])
category_service = CategoryService()
utils = Utilities()

@category_router.get('/')
async def get_categories(search: str | None = None, from_date: str | None = None, to_date: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    return category_service.get_categories(db=db, username=str(current_user.username), search=search, from_date=from_date, to_date=to_date)



@category_router.post('/add', response_model=CategoryOut)
async def create_category(data: CategoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    return category_service.create_category(db=db, username=current_user.username, title=data.title, description=data.description)
# role-based access
@category_router.put('/update', response_model=CategoryOut)
async def update_category(data: CategoryUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    owner_username = utils.get_user_permissions(current_user=current_user, data=data)
    return category_service.update_category(db=db, owner_username=owner_username, category_id=data.category_id, new_title=data.new_title, new_description=data.new_description)

# role-based access
@category_router.delete('/delete')
async def delete_category(data: CategoryDelete, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    owner_username = utils.get_user_permissions(current_user=current_user, data=data)
    return category_service.delete_category(db=db, owner_username=owner_username, category_id=data.category_id)


@category_router.post('/{category_id}')
async def get_single_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _: None = Depends(rate_limit)):
    return category_service.get_single_category(db=db, owner_username=str(current_user.username), category_id=category_id)






from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.auth import get_current_user, rate_limit
from app.services.profile_service import ProfileService
from app.schemas.user_schemas import UserOut, UserUpdate
from app.models.user_model import User

profile_router = APIRouter(prefix='/profile', tags=['Profile'])
profile_service = ProfileService()

@profile_router.get('/', response_model=UserOut)
async def get_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _: None = Depends(rate_limit)):
    return profile_service.get_profile(db=db, user_id=current_user.id)

@profile_router.post('/update', response_model=UserOut)
async def update_profile(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _: None = Depends(rate_limit)):
    return profile_service.update_profile(db=db, user_id=current_user.id, new_username=data.new_username, new_email=data.email)




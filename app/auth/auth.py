from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth_config import oauth2_scheme
from app.services.auth_service import AuthService
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate, UserOut
# redis client
from app.core.redis import redis_client, JWT_EXPIRATION_TIME
# user model
from app.models.user_model import User
import redis
import logging

logger = logging.getLogger(__name__)
auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    token = auth_service.login_user(db=db, username=form_data.username, password=form_data.password)
    return token


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:

        if redis_client.get(f'blacklisted:{token}'):
            raise HTTPException(status_code=401, detail='Token revoked')

        return auth_service.get_current_user(db=db, token=token)
    except redis.RedisError:
        logger.exception('Redis unavailable')
        raise HTTPException(status_code=503, detail='Redis unavailable')


def rate_limit(current_user: User = Depends(get_current_user)):

    try:
        key = f'rate_limit:{current_user.id}'

        requests = redis_client.incr(key)

        if requests == 1:
            redis_client.expire(key, 60)

        if requests > 100:
            raise HTTPException(status_code=429, detail='Too many requests')
    except redis.RedisError:
        raise HTTPException(status_code=503, detail='Redis unavailable')

def anonymous_rate_limit():
    try:
        key = f'anonymous_rate_limit'

        requests = redis_client.incr(key)

        if requests == 1:
            redis_client.expire(key, 60)

        if requests > 30:
            raise HTTPException(status_code=429, detail='Too many requests')
    except redis.RedisError:
        raise HTTPException(status_code=503, detail='Redis unavailable')







@auth_router.post('/logout')
async def logout(token: str = Depends(oauth2_scheme), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    redis_client.set(f'blacklisted:{token}', '1', ex=JWT_EXPIRATION_TIME)

    return {'status': 'ok'}






@auth_router.post('/register', response_model=UserOut)
async def register(data: UserCreate, db: Session = Depends(get_db)):

    return auth_service.create_user(db=db, username=data.username, password=data.password, role=data.role, email=data.email)




@auth_router.get('/me', response_model=UserOut)
async def read_current_user(current_user = Depends(get_current_user)):
    return current_user





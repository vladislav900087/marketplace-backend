import jwt

from fastapi import HTTPException, status
from app.auth.auth_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from app.models.user_model import User
from pwdlib import PasswordHash
# send email tasks
from app.tasks.email_tasks import send_welcome_email

class AuthService:
    def __init__(self):
        self.pwd_hasher = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self.pwd_hasher.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_hasher.verify(plain_password, hashed_password)

    def create_user(self, db, username: str, password: str, role: str, email: str | None = None) -> User:
        if role not in ('admin', 'user'):
            raise HTTPException(400, detail='Invalid role')

        existing_username = db.query(User).filter(User.username == username).first()
        if existing_username:
            raise HTTPException(400, 'User already exists')

        if email:
            existing_email = db.query(User).filter(User.email == email).first()
            if existing_email:
                raise HTTPException(400, 'Email already exists')

        new_user = User(username=username, email=email, role=role, password=self.hash_password(password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        send_welcome_email.delay(to=new_user.email)



        return new_user

    def authenticate_user(self, db, username: str, password: str) -> User:
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return None

        if not self.verify_password(password, user.password):
            return None

        return user

    def login_user(self, db, username: str, password: str):
        user = self.authenticate_user(db, username, password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

        token = self.create_access_token(username, user.role)

        return {'access_token': token, 'token_type': 'bearer'}

    def create_access_token(self, username: str, role: str) -> str:
        payload = {
            'sub': username,
            'role': role,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload['sub'], payload['role']

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    def get_current_user(self, db, token: str) -> User:
        username, role = self.decode_access_token(token)

        user = db.query(User).filter(User.username == username).filter(User.role == role).first()
        if not user:
            raise HTTPException(status_code=404, detail='User not found')



        return user
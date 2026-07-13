from datetime import datetime
from app.models.user_model import User
from fastapi import HTTPException, status

class Utilities:
    def get_current_user(self, db, username: str | None = None, user_id: int | None = None) -> User:
        if username:
            current_user = db.query(User).filter(User.username == username).first()
            if not current_user:
                return None
            return current_user
        if user_id:
            current_user = db.query(User).filter(User.id == user_id).first()
            if not current_user:
                return None
            return current_user

        if not username and user_id is None:
            return None



    def is_valid_date(self, date_string: str, date_format: str = '%Y-%m-%d') -> bool:
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False
    def turn_string_to_datetime(self, datetime_str: str) -> datetime | None:
        if self.is_valid_date(datetime_str):
            datetime_obj = datetime.fromisoformat(datetime_str)

            return datetime_obj
        else:
            return None

    def get_user_permissions(self, current_user, data):
        owner_username = current_user.username
        if current_user.role == 'admin':
            owner_username = data.owner_username

        return owner_username

    def add_to_db(self, db, item):
        db.add(item)
        db.commit()
        db.refresh(item)

    def if_not_user(self, current_user):
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

from fastapi import Depends, HTTPException
from app.models.user_model import User
# utils
from app.services.utilities import Utilities

class ProfileService:
    def __init__(self):
        self.utils = Utilities()

    def get_profile(self, db, user_id):
        current_user = db.query(User).filter(User.id == user_id).first()
        self.utils.if_not_user(current_user)

        return current_user

    def update_profile(self, db, user_id: int, new_username: str | None = None, new_email: str | None = None):
        current_user = db.query(User).filter(User.id == user_id).first()
        self.utils.if_not_user(current_user)

        if new_username:
            current_user.username = new_username
        elif new_email:
            current_user.email = new_email

        db.commit()

        return current_user
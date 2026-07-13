from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.models.category_model import Category
from app.services.utilities import Utilities
from operator import or_
# redis client
from app.core.redis import redis_client, EXPIRATION_TIME


import json




class CategoryService:
    def __init__(self):
        self.utils = Utilities()

    def create_category(self, db, username, title: str, description: str | None = None) -> Category:

        current_user = self.utils.get_current_user(db=db, username=username)

        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        category_timestamp = datetime.now(timezone.utc)
        new_category = Category(title=title, description=description, owner_id=current_user.id, created_at=category_timestamp, updated_at=category_timestamp)

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        redis_client.delete(f'categories: {username}')

        return new_category

    def get_categories(self, db, username: str, search: str | None = None, from_date: str | None = None, to_date: str | None = None):
        current_user = self.utils.get_current_user(db=db, username=username)

        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        owner_username = str(current_user.username)

        cached = redis_client.get(f'categories: {owner_username}')
        if cached:
            return json.loads(cached)



        query = db.query(Category).filter(Category.owner_id == current_user.id)

        if search:
            pattern = f'%{search}%'
            query = query.filter(or_(Category.title.ilike(pattern), Category.description.ilike(pattern)))

        if from_date:
            from_date = self.utils.turn_string_to_datetime(from_date)
            if from_date is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid date format')

            query = query.filter(Category.created_at >= from_date)
        if to_date:
            to_date = self.utils.turn_string_to_datetime(to_date)
            if to_date is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid date format')

            query = query.filter(Category.created_at <= to_date)

        category_dicts = [{'id': category.id, 'title': category.title, 'description': category.description, 'created_at': category.created_at.strftime('%Y-%m-%d %H:%M:%S'), 'updated_at': category.updated_at.strftime('%Y-%m-%d %H:%M:%S')} for category in list(query.all())]
        redis_client.set(f'categories: {owner_username}', json.dumps(category_dicts))


        return category_dicts

    def get_single_category(self, db, owner_username: str, category_id: int):
        current_user = self.utils.get_current_user(db=db, username=owner_username)
        self.utils.if_not_user(current_user)

        cached = redis_client.get(f'category: {category_id}')
        if cached:
            return json.loads(cached)

        category = db.query(Category).filter(Category.owner_id == current_user.id).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category does not exist')

        category_dict = {'id': category.id, 'title': category.title, 'description': category.description, 'created_at': category.created_at.strftime('%Y-%m-%d %H:%M:%S'), 'updated_at': category.updated_at.strftime('%Y-%m-%d %H:%M:%S')}
        redis_client.set(f'category: {category.id}', json.dumps(category_dict))

        return category_dict




    def update_category(self, db, owner_username, category_id: int, new_title: str | None = None, new_description: str | None = None):
        current_user = self.utils.get_current_user(db=db, username=owner_username)
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        category = db.query(Category).filter(Category.owner_id == current_user.id).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

        if new_title:
            category.title = new_title
        if new_description:
            category.description = new_description

        timestamp = datetime.now(timezone.utc)
        category.updated_at = timestamp

        db.commit()

        redis_client.delete(f'category: {category_id}')

        return category

    def delete_category(self, db, owner_username, category_id: int):
        current_user = self.utils.get_current_user(db=db, username=owner_username)
        if not current_user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='User not found')

        category = db.query(Category).filter(Category.owner_id == current_user.id).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Category not found')

        db.delete(category)
        db.commit()

        redis_client.delete(f'category: {category_id}')

        return {'category_id': category_id, 'status': 'deleted'}












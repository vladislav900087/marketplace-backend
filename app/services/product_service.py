from typing import Optional
# redis client
from app.core.redis import redis_client, EXPIRATION_TIME



from app.models.user_model import User
from app.models.product_model import Product
from app.models.category_model import Category
from datetime import datetime, timezone
from fastapi import HTTPException



import json



class ProductService:
    def create_product(self, db, title: str, price: float, currency: str, owner_username: str,  description: Optional[str] = None, category_id: Optional[int] = None):

        owner = db.query(User).filter(User.username == owner_username).first()
        if not owner:
            raise ValueError('Owner does not exist')

        created_at = datetime.now(timezone.utc)
        product = Product(title=title, price=price, currency=currency, owner_id=owner.id, created_at=created_at, updated_at=created_at)

        if category_id:
            category = db.query(Category).filter(Category.id == category_id).first()
            if category:
                product.category_id = category.id

        if description:
            product.description = description

        db.add(product)
        db.commit()
        db.refresh(product)

        redis_client.delete(f'products: {owner_username}')

        return product
    def get_all_products(self, db, owner_username: str):

        owner = db.query(User).filter(User.username == owner_username).first()
        if not owner:
            raise ValueError('Owner does not exist')

        owner_username = str(owner.username)

        cached = redis_client.get(f'products: {owner_username}')
        if cached:
            return json.loads(cached)

        products_from_db = db.query(Product).filter(Product.owner_id == owner.id).all()
        product_dicts = [{'id': product.id, 'title': product.title, 'description': product.description, 'currency': product.currency, 'price': product.price, 'category_id': product.category_id} for product in list(products_from_db)]
        redis_client.set(f'products: {owner_username}', json.dumps(product_dicts), ex=EXPIRATION_TIME)


        return product_dicts

    def get_single_product(self, db, product_id: int):

        cached = redis_client.get(f'product: {product_id}')
        if cached:
            return json.loads(cached)
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError('Product does not exist')

        product_dict = {'id': product.id, 'title': product.title, 'description': product.description, 'currency': product.currency, 'price': product.price, 'category_id': product.category_id}
        redis_client.set(f'product: {product.id}', json.dumps(product_dict), ex=EXPIRATION_TIME)


        return product_dict

    def update_product(self, db, owner_username: str, product_id: int, new_title, new_description: Optional[str] = None, new_price: Optional[float] = None, new_currency: Optional[str] = None, new_category_id: Optional[int] = None):

        owner = db.query(User).filter(User.username == owner_username).first()
        if not owner:
            raise ValueError('Owner does not exist')

        product = db.query(Product).filter(Product.owner_id == owner.id).filter(Product.id == product_id).first()

        if not product:
            raise ValueError('Product does not exist')

        if new_title:
            product.title = new_title
        if new_description:
            product.description = new_description

        if new_category_id:
            category = db.query(Category).filter(Category.owner_id == owner.id).filter(Category.id == new_category_id).first()
            if category:
                product.category_id = category.id

        if new_price:
            product.price = new_price

        if new_currency:
            product.currency = new_currency

        updated_at = datetime.now(timezone.utc)

        product.updated_at = updated_at

        db.commit()

        redis_client.delete(f'product: {product_id}')
        redis_client.delete(f'products: {owner_username}')

        return {product.title: 'updated successfully'}

    def delete_product(self, db, owner_username: str, product_id: int):
        owner = db.query(User).filter(User.username == owner_username).first()
        if not owner:
            raise ValueError('Owner does not exist')
        product = db.query(Product).filter(Product.owner_id == owner.id).filter(Product.id == product_id).first()
        if not product:
            raise ValueError('Product does not exist')

        db.delete(product)
        db.commit()

        redis_client.delete(f'product: {product_id}')
        redis_client.delete(f'products: {owner_username}')

        return {'product_id': product_id, 'status': 'deleted'}

    def get_current_error(self, e):
        if 'does not exist' in str(e):
            if 'Owner' in str(e):
                message = 'Owner not found'
            if 'Product' in str(e):
                message = 'Product not found'

            status_code = 404

            return message, status_code
        else:
            message = str(e)
            status_code = 500

            return message, status_code

    def raise_error(self, e):
        message, status_code = self.get_current_error(e)

        raise HTTPException(status_code=status_code, detail=message)

    def get_user_permissions(self, current_user_username: str, current_user_role: str, product_data):
        owner_username = current_user_username
        if current_user_role == 'admin':
            owner_username = product_data.owner_username

        return owner_username




















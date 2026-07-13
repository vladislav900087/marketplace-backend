# utilities for the service
from app.services.utilities import Utilities
# fastapi error tools
from fastapi import HTTPException, status
# models
from app.models.product_model import Product
from app.models.cart_models import Cart, CartItem
# datetime
from datetime import datetime, timezone

class CartService:
    def __init__(self):
        self.utils = Utilities()
    def add_to_cart(self, db, username: str, product_id: int, quantity: int = 1):
        current_user = self.utils.get_current_user(db=db, username=username)
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
        if product.owner_id == current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You cannot order your own product')

        timestamp = datetime.now(timezone.utc)
        user_cart = db.query(Cart).filter(Cart.owner_id == current_user.id).first()
        if not user_cart:
            user_cart = Cart(owner_id=current_user.id, created_at=timestamp)
            db.add(user_cart)
            db.commit()
            db.refresh(user_cart)
            user_cart = db.query(Cart).filter(Cart.owner_id == current_user.id).first()
        if quantity == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quantity is 0')

        cart_item = db.query(CartItem).filter(CartItem.cart_id == user_cart.id).filter(CartItem.product_id == product.id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=user_cart.id, product_id=product.id, quantity=quantity)

            db.add(cart_item)
        db.commit()
        db.refresh(cart_item)

        return {
            'product_id': cart_item.product_id,
            'title': product.title,
            'price': product.price,
            'quantity': cart_item.quantity,
            'subtotal': product.price * cart_item.quantity

        }

    def get_user_cart(self, db, username: str):
        current_user = self.utils.get_current_user(db=db, username=username)
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        cart = db.query(Cart).filter(Cart.owner_id == current_user.id).first()
        if not cart:
            user_cart = Cart(owner_id=current_user.id, created_at=datetime.now(timezone.utc))
            db.add(user_cart)
            db.commit()
            db.refresh(user_cart)

            cart = db.query(Cart).filter(Cart.owner_id == current_user.id).first()

        base_return_format = {'items': [], 'total_price': 0}
        items = []
        prices = []
        if len(cart.products) != 0:
            for product_cart_item in cart.products:
                product_in_db = db.query(Product).filter(Product.id == product_cart_item.product_id).first()
                if not product_in_db:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
                items.append({'product_id': product_in_db.id, 'title': product_in_db.title, 'price': product_in_db.price, 'quantity': product_cart_item.quantity, 'subtotal': product_in_db.price * product_cart_item.quantity})
                prices.append(product_in_db.price * product_cart_item.quantity)

            total_price = sum(prices)
            base_return_format['items'] = items
            base_return_format['total_price'] = total_price
            cart_result = base_return_format
            return cart_result
        else:
            return base_return_format


    def remove_from_cart(self, db, username: str, product_id: int):
        current_user = self.utils.get_current_user(db=db, username=username)
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        cart = db.query(Cart).filter(Cart.owner_id == current_user.id).first()
        if not cart:
            user_cart = Cart(owner_id=current_user.id, created_at=datetime.now(timezone.utc))
            db.add(user_cart)
            db.commit()
            db.refresh(user_cart)

            cart = db.query(Cart).filter(Cart.owner_id == current_user.id).first()

        product_in_db = db.query(Product).filter(Product.id == product_id).first()
        if not product_in_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

        product_in_cart = db.query(CartItem).filter(CartItem.cart_id == cart.id).filter(CartItem.product_id == product_in_db.id).first()
        if not product_in_cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

        db.delete(product_in_cart)
        db.commit()

        return {'product_id': product_id, 'status': 'deleted'}

    def clear_cart(self, db, username: str):
        current_user = self.utils.get_current_user(db=db, username=username)
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        cart = db.query(Cart).filter(Cart.owner_id == current_user.id).first()
        if not cart:
            new_user_cart = Cart(owner_id=current_user.id, created_at=datetime.now(timezone.utc))
            db.add(new_user_cart)
            db.commit()
            db.refresh(new_user_cart)

            cart = db.query(Cart).filter(Cart.owner_id == current_user.id).first()


        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()

        return {username: 'Your cart has been cleared'}










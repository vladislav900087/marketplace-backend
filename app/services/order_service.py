# fastapi tools
from fastapi import HTTPException, status
# models
from app.models.cart_models import Cart, CartItem
from app.models.order_models import Order, OrderItem
from app.models.product_model import Product
# utilities
from app.services.utilities import Utilities
# cart services
from app.services.cart_service import CartService
# datetime
from datetime import datetime, timezone
# confirmation email message
from app.tasks.email_tasks import send_order_confirmation_email

from app.tasks.result_tasks import generate_pdf_invoice
import logging

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self):
        self.utils = Utilities()
        self.cart_service = CartService()
    def create_order(self, db,  username: str):
        current_user = self.utils.get_current_user(db=db, username=username)
        self.utils.if_not_user(current_user)

        cart = db.query(Cart).filter(Cart.owner_id == current_user.id).first()
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You don\'t have any products in your cart. Try adding ones before proceeding to order')

        user_order = Order(user_id=current_user.id, status='pending', total_price=0, created_at=datetime.now(timezone.utc))
        self.utils.add_to_db(db=db, item=user_order)

        # getting products from the user's cart to create an order
        all_prices = []
        if len(cart.products) != 0:
            for product_in_cart in cart.products:
                product_in_db = db.query(Product).filter(Product.id == product_in_cart.product_id).first()
                if not product_in_db:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product does not exist')
                all_prices.append(product_in_db.price * product_in_cart.quantity)

                order_item = OrderItem(product_id=product_in_cart.product_id, quantity=product_in_cart.quantity, price_at_purchase=product_in_db.price, order_id=user_order.id)
                self.utils.add_to_db(db=db, item=order_item)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You don\'t have any products in your cart')
        # getting a total price of all the products the user has chosen
        if len(all_prices) != 0:
            total_price = sum(all_prices)
        else:
            total_price = 0

        # updating the total price of the user's order
        user_order.total_price = total_price

        db.commit()
        db.refresh(user_order)

        # clear the user's cart when the order is created yet
        if len(cart.products) != 0:
            self.cart_service.clear_cart(db=db, username=str(current_user.username))
        try:
            generate_pdf_invoice.delay(user_id=current_user.id, order_id=user_order.id)
        except Exception as e:
            logger.exception(f'Could not enqueue invoice generation: {e}')

        return user_order


    def process_order(self, db,  username: str, order_id: int, is_paid: bool, is_cancelled: bool):
        current_user = self.utils.get_current_user(db=db, username=username)
        self.utils.if_not_user(current_user)


        order = db.query(Order).filter(Order.user_id == current_user.id).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order does not exist')

        if is_paid:
            order.status = 'paid'

        if is_cancelled:
            order.status = 'cancelled'

        db.commit()




    def confirm_order(self, db, username: str, order_id: int, action: str):
        current_user = self.utils.get_current_user(db=db, username=username)
        self.utils.if_not_user(current_user)



        current_order = db.query(Order).filter(Order.user_id == current_user.id).filter(Order.id == order_id).first()
        if not current_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order does not exist')


        if action not in ('pay', 'cancel'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid action')




        if action == 'pay':
            self.process_order(db=db, username=str(current_user.username), order_id=current_order.id, is_paid=True, is_cancelled=False)


        elif action == 'cancel':
            self.process_order(db=db, username=str(current_user.username), order_id=current_order.id, is_paid=False, is_cancelled=True)

        try:
            send_order_confirmation_email.delay(to=current_user.email)
        except Exception as e:
            logger.exception(f'could enqueue confirmation email: {e}')
        return current_order

    def get_user_orders(self, db, username: str):
        current_user = self.utils.get_current_user(db=db, username=username)
        self.utils.if_not_user(current_user)

        orders = db.query(Order).filter(Order.user_id == current_user.id).all()

        return {'items': orders}

    def get_user_order(self, db, username: str, order_id: int):
        current_user = self.utils.get_current_user(db=db, username=username)
        self.utils.if_not_user(current_user)

        order = db.query(Order).filter(Order.user_id == current_user.id).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order does not exist')

        return order





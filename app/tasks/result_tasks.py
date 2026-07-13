from app.core.celery_app import celery_app
from app.services.pdf_service import PDFService
from app.core.database import SessionLocal
from app.models.order_models import Order, OrderItem
from app.models.user_model import User
from app.models.product_model import Product
from app.models.category_model import Category
from app.models.cart_models import Cart, CartItem

@celery_app.task
def generate_pdf_invoice(user_id: int, order_id: int):

    db = SessionLocal()

    pdf_service = PDFService()

    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError('User not found')
        order = db.query(Order).filter(Order.user_id == user.id).filter(Order.id == order_id).first()
        if not order:
            raise ValueError('Order not found')

        pdf_service.generate_invoice(order)

    finally:
        db.close()


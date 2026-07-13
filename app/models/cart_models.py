# sql alchemy imports
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
# db imports
from app.core.database import Base
# models
from app.models.product_model import Product

# datetime
from datetime import datetime, timezone

class Cart(Base):
    __tablename__ = 'cart'
    # model columns
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    # relationships
    owner: Mapped['User'] = relationship(back_populates='user_cart')
    products: Mapped[list['CartItem']] = relationship(back_populates='product_cart')



class CartItem(Base):
    __tablename__ = 'cart_items'
    # model columns
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(default=0)
    # relationship
    product_cart: Mapped['Cart'] = relationship(back_populates='products')


# sqlalchemy tools
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
# db instances
from app.core.database import Base
# datetime
from datetime import datetime, timezone

class Order(Base):
    __tablename__ = 'orders'

    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str] = mapped_column(nullable=False)
    total_price: Mapped[float] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    # relationships
    owner: Mapped['User'] = relationship(back_populates='orders')
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'

    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)
    price_at_purchase: Mapped[float] = mapped_column(default=0, nullable=False)

    # relationships
    order: Mapped['Order'] = relationship(back_populates='order_items')


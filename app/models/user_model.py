from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import datetime


class User(Base):
    __tablename__ = 'users'
    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(unique=True, nullable=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(datetime.UTC))
    updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(datetime.UTC))
    # relationship
    products: Mapped[list["Product"]] = relationship(back_populates='owner')
    categories: Mapped[list['Category']] = relationship(back_populates='owner')
    user_cart: Mapped['Cart'] = relationship(back_populates='owner')
    orders: Mapped[list['Order']] = relationship(back_populates='owner')



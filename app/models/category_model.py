from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import datetime

class Category(Base):
    __tablename__ = 'categories'
    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    # relationships
    owner: Mapped['User'] = relationship(back_populates='categories')
    products: Mapped[list['Product']] = relationship(back_populates='category')

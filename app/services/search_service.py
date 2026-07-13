from math import ceil
from sqlalchemy import or_
# models
from app.models.product_model import Product
from app.models.category_model import Category



class SearchService:
    def search_all_products(self, db, search: str | None = None, sort: str | None = None, category_id: int | None = None, page: int = 1, limit: int = 20):

        query = db.query(Product)
        if search:
            pattern = f'%{search}%'
            query = query.filter(or_(Product.title.ilike(pattern), Product.description.ilike(pattern)))

        if category_id:
            query = query.filter(Product.category_id == category_id)

        total = query.count()

        if sort == 'price_asc':
            query = query.order_by(Product.price.asc())
        elif sort == 'price_desc':
            query = query.order_by(Product.price.desc())
        else:
            query = query.order_by(Product.created_at.desc())

        offset = self.calculate_offset(page=page, limit=limit)

        items = query.offset(offset).limit(limit).all()

        return {
            'items': items,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': ceil(total / limit) if total else 0
        }












    def calculate_offset(self, page, limit):
        offset = (page - 1) * limit
        return offset





from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.search_service import SearchService
from app.schemas.product_schemas import ProductListResponse
# rate limit for unauthorized user
from app.auth.auth import anonymous_rate_limit

search_router = APIRouter(prefix='/marketplace', tags=['Marketplace'])
search_service = SearchService()

@search_router.get('/products/public', response_model=ProductListResponse)
async def search_products(search: str | None = None, category_id: int | None = None, sort: str = 'newest', page: int = 1, limit: int = 20, db: Session = Depends(get_db), _: None = Depends(anonymous_rate_limit)):
    return search_service.search_all_products(db=db, search=search, category_id=category_id, page=page, limit=limit, sort=sort)



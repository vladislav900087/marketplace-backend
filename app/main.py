# core fastapi tools
from fastapi import FastAPI
# cors for the frontend
from fastapi.middleware.cors import CORSMiddleware
# database
from app.core.database import Base, engine
# api routers
from app.auth.auth import auth_router
from app.api.product_api import product_router
from app.api.category_api import category_router
from app.api.search_api import search_router
from app.api.cart_api import cart_router
from app.api.order_api import order_router
from app.api.profile_api import profile_router




app = FastAPI()
# add middleware
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# add routers
app.include_router(auth_router, tags=['Authentication'])
app.include_router(product_router, tags=['Products'])
app.include_router(category_router, tags=['Categories'])
app.include_router(search_router, tags=['Search'])
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(profile_router)


Base.metadata.create_all(bind=engine)


@app.get('/')
async def root():
    return {'message': 'This is my marketplace!'}




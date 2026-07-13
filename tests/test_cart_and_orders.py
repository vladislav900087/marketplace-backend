from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from tests.test_db import override_get_db, test_engine, Base
from tests.services import ServicesForTest
import random
# models
from app.models.user_model import User
from app.models.category_model import Category
from app.models.product_model import Product
from app.models.cart_models import Cart, CartItem
from app.models.order_models import Order, OrderItem

Base.metadata.create_all(bind=test_engine)

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
service = ServicesForTest()


def test_cart_and_order_system():
    user = service.create_random_user()
    buyer = service.create_random_user()
    r1 = client.post('/register', json=user)

    assert r1.status_code == 200

    r2 = client.post('/login', data={'username': user['username'], 'password': user['password']})
    assert r2.status_code == 200
    token = r2.json()['access_token']

    r3 = client.post('/register', json=buyer)
    assert r3.status_code == 200

    r4 = client.post('/login', data={'username': buyer['username'], 'password': buyer['password']})
    assert r4.status_code == 200

    buyer_token = r4.json()['access_token']

    random_product = service.create_random_product()
    r5 = client.post('/products', json=random_product, headers={'Authorization': f'Bearer {token}'})
    assert r5.status_code == 200

    product_id = r5.json()['id']

    r6 = client.post('/cart/add', json={'product_id': product_id, 'quantity': random.randint(1, 5)}, headers={'Authorization': f'Bearer {buyer_token}'})
    assert r4.status_code == 200



    r7 = client.get('/cart/items', headers={'Authorization': f'Bearer {buyer_token}'})

    assert r7.status_code == 200

    r8 = client.post('/orders/add', headers={'Authorization': f'Bearer {buyer_token}'})
    assert r6.status_code == 200

    order_id = r8.json()['id']
    action = random.choice(('pay', 'cancel'))

    r9 = client.post('/orders/confirm', json={'order_id': order_id, 'action': action}, headers={'Authorization': f'Bearer {buyer_token}'})
    assert r9.status_code == 200

    r10 = client.get('/orders/', headers={'Authorization': f'Bearer {buyer_token}'})
    assert r10.status_code == 200






from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from tests.test_db import test_engine, Base, override_get_db
from tests.services import ServicesForTest
import random
# models
from app.models.user_model import User
from app.models.product_model import Product
from app.models.category_model import Category
from app.models.cart_models import Cart, CartItem
from app.models.order_models import Order, OrderItem


Base.metadata.create_all(bind=test_engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
service = ServicesForTest()


def test_add_product():
    user = service.create_random_user()
    r1 = client.post('/register', json=user)
    assert r1.status_code == 200

    r2 = client.post('/login', data={'username': user['username'], 'password': user['password']})
    assert r2.status_code == 200
    token = r2.json()['access_token']
    random_product = service.create_random_product()
    r3 = client.post('/products', json=random_product, headers={'Authorization': f'Bearer {token}'})
    assert r3.status_code == 200

def test_update_product():
    user = service.create_random_user()
    r1 = client.post('/register', json=user)
    assert r1.status_code == 200

    r2 = client.post('/login', data={'username': user['username'], 'password': user['password']})
    assert r2.status_code == 200

    token = r2.json()['access_token']
    random_product = service.create_random_product()
    r3 = client.post('/products', json=random_product, headers={'Authorization': f'Bearer {token}'})
    assert r3.status_code == 200
    product_id = r3.json()['id']
    product_update = {'owner_username': user['username'], 'new_title': None, 'new_description': 'updated_description', 'new_price': random.randint(1, 100), 'new_currency': None, 'new_category_id': None}

    r4 = client.put(f'/products/{product_id}', params={'product_id': product_id}, json=product_update, headers={'Authorization': f'Bearer {token}'})
    assert r4.status_code == 200



def test_get_products():
    user = service.create_random_user()
    r1 = client.post('/register', json=user)
    assert r1.status_code == 200
    r2 = client.post('/login', data={'username': user['username'], 'password': user['password']})
    assert r2.status_code == 200
    token = r2.json()['access_token']

    random_product = service.create_random_product()
    r3 = client.post('/products', json=random_product, headers={'Authorization': f'Bearer {token}'})
    assert r3.status_code == 200
    product_id = r3.json()['id']

    r4 = client.get(f'/products/{product_id}', headers={'Authorization': f'Bearer {token}'})
    assert r4.status_code == 200

    r5 = client.get('/products', headers={'Authorization': f'Bearer {token}'})
    assert r5.status_code == 200

    print(r5.json())
    print(r5.text)

def test_delete_product():
    user = service.create_random_user()
    r1 = client.post('/register', json=user)
    assert r1.status_code == 200
    r2 = client.post('/login', data={'username': user['username'], 'password': user['password']})
    assert r2.status_code == 200
    token = r2.json()['access_token']

    random_product = service.create_random_product()
    r3 = client.post('products', json=random_product, headers={'Authorization': f'Bearer {token}'})
    assert r3.status_code == 200
    product_id = r3.json()['id']

    r4 = client.request('DELETE', f'/products/{product_id}', params={'product_id': product_id}, json={'owner_username': user['username']}, headers={'Authorization': f'Bearer {token}'})
    assert r4.status_code == 200
    print(r4.json())






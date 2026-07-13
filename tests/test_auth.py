from fastapi.testclient import TestClient
# test services and db functions
from tests.services import ServicesForTest
from tests.test_db import test_engine, Base, override_get_db
from app.core.database import get_db
# models
from app.models.product_model import Product
from app.models.category_model import Category
from app.models.user_model import User
from app.models.cart_models import *
from app.models.order_models import Order
# main app
from app.main import app

Base.metadata.create_all(bind=test_engine)
print('Tables created')

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
service = ServicesForTest()


def test_user_register():
    user = service.create_random_user()
    response = client.post('/register', json=user)
    assert response.status_code == 200
    print(response.text)




def test_login_success():

    user = service.create_random_user()
    r1 = client.post('/register', json=user)
    assert r1.status_code == 200

    r2 = client.post('/login', data={'username': user['username'], 'password': user['password']})
    assert r2.status_code == 200
    print(r2.text)

    assert 'access_token' in r2.json()


def test_logout_success():
    user = service.create_random_user()
    r1 = client.post('/register', json=user)
    assert r1.status_code == 200

    r2 = client.post('/login', data={'username': user['username'], 'password': user['password']})
    assert r2.status_code == 200
    token = r2.json()['access_token']
    r3 = client.post('/logout', headers={'Authorization': f'Bearer {token}'})
    assert r3.status_code == 200

    print(r3.text)
    print(r3.json())



def test_invalid_credentials():
    user = service.create_random_user()
    r1 = client.post('/register', json=user)
    assert r1.status_code == 200
    r2 = client.post('/login', data={'username': user['username'], 'password': 'wrong_password'})

    assert r2.status_code == 401
    print(r2.text)

def test_protected_route():
    user = service.create_random_user()
    r1 = client.post('/register', json=user)
    assert r1.status_code == 200
    r2 = client.post('/login', data={'username': user['username'], 'password': user['password']})
    assert r2.status_code == 200
    token = r2.json()['access_token']
    r3 = client.get('/me', headers={'Authorization': f'Bearer {token}'})
    assert r3.status_code == 200
    print(r3.text)




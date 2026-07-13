# modules
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from tests.test_db import override_get_db, Base, test_engine
import random
import uuid

# models
from app.models.user_model import User
from app.models.product_model import Product
from app.models.category_model import Category
from app.models.cart_models import Cart, CartItem
from app.models.order_models import Order, OrderItem
# test service
from tests.services import ServicesForTest

Base.metadata.create_all(bind=test_engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
service = ServicesForTest()


# test whether the admin is able to update someone's else product
def test_update_some_product():
    admin_user = service.create_admin_user()
    just_user = service.create_user()
    r1 = client.post('/register', json=admin_user)
    assert r1.status_code == 200

    r2 = client.post('/register', json=just_user)
    assert r2.status_code == 200

    r3 = client.post('/login', data={'username': just_user['username'], 'password': just_user['password']})
    assert r3.status_code == 200

    just_user_token = r3.json()['access_token']

    any_product = service.create_random_product()
    r4 = client.post('/products', json=any_product, headers={'Authorization': f'Bearer {just_user_token}'})
    assert r4.status_code == 200

    product_id = r4.json()['id']

    r5 = client.post('/login', data={'username': admin_user['username'], 'password': admin_user['password']})
    assert r5.status_code == 200
    admin_token = r5.json()['access_token']

    updated_product = {'owner_username': just_user['username'], 'new_title': None, 'new_description': 'Any new description', 'new_price': random.randint(1, 100), 'new_currency': random.choice(('USD', 'EUR', 'RUB', 'KZT')), 'new_category_id': None}

    r6 = client.put(f'/products/{product_id}', json=updated_product, headers={'Authorization': f'Bearer {admin_token}'})
    assert r6.status_code == 200

# test whether the user is able to update one's own product

def test_update_own_product():
    just_user = service.create_user()
    r1 = client.post('/register', json=just_user)
    assert r1.status_code == 200
    r2 = client.post('/login', data={'username': just_user['username'], 'password': just_user['password']})
    assert r2.status_code == 200
    just_user_token = r2.json()['access_token']

    random_product = service.create_random_product()
    r3 = client.post('/products', json=random_product, headers={'Authorization': f'Bearer {just_user_token}'})
    assert r3.status_code == 200
    product_id = r3.json()['id']
    updated_product = {'owner_username': None, 'new_title': None, 'new_description': 'Some new description', 'new_price': random.randint(1, 100), 'new_category_id': None, 'new_currency': random.choice(('USD', 'EUR', 'RUB', 'KZT'))}
    r4 = client.put(f'/products/{product_id}', json=updated_product, headers={'Authorization': f'Bearer {just_user_token}'})
    assert r4.status_code == 200

# test whether the admin is able to delete someone's else product
def test_delete_some_product():
    admin_user = service.create_admin_user()
    just_user = service.create_user()

    r1 = client.post('/register', json=admin_user)
    assert r1.status_code == 200

    r2 = client.post('/register', json=just_user)
    assert r2.status_code == 200

    r3 = client.post('/login', data={'username': just_user['username'], 'password': just_user['password']})
    assert r3.status_code == 200
    just_user_token = r3.json()['access_token']

    random_product = service.create_random_product()

    r4 = client.post('/products', json=random_product, headers={'Authorization': f'Bearer {just_user_token}'})
    assert r4.status_code == 200
    product_id = r4.json()['id']

    r5 = client.post('/login', data={'username': admin_user['username'], 'password': admin_user['password']})
    assert r5.status_code == 200
    admin_token = r5.json()['access_token']
    owner_username = {'owner_username': just_user['username']}
    r6 = client.request('DELETE', f'/products/{product_id}', json=owner_username, headers={'Authorization': f'Bearer {admin_token}'})
    assert r6.status_code == 200

# test whether the user is able to delete one's own product
def test_delete_own_product():
    just_user = service.create_user()
    r1 = client.post('/register', json=just_user)
    assert r1.status_code == 200

    r2 = client.post('/login', data={'username': just_user['username'], 'password': just_user['password']})
    assert r2.status_code == 200
    just_user_token = r2.json()['access_token']

    random_product = service.create_random_product()

    r3 = client.post('/products', json=random_product, headers={'Authorization': f'Bearer {just_user_token}'})
    assert r3.status_code == 200
    product_id = r3.json()['id']
    owner_username = {'owner_username': None}
    r4 = client.request('DELETE', f'/products/{product_id}', json=owner_username, headers={'Authorization': f'Bearer {just_user_token}'})
    assert r4.status_code == 200

# test whether the user tried to update or delete someone's else product
def test_product_not_found_error():
    just_first_user = service.create_user()
    just_second_user = service.create_user()
    r1 = client.post('/register', json=just_first_user)
    assert r1.status_code == 200

    r2 = client.post('/register', json=just_second_user)
    assert r2.status_code == 200

    r3 = client.post('/login', data={'username': just_first_user['username'], 'password': just_first_user['password']})
    assert r3.status_code == 200
    just_first_user_token = r3.json()['access_token']

    random_product = service.create_random_product()

    r4 = client.post('/products', json=random_product, headers={'Authorization': f'Bearer {just_first_user_token}'})
    assert r4.status_code == 200

    product_id = r4.json()['id']
    uid = uuid.uuid4().hex[:8]

    updated_product = {'owner_username': just_first_user['username'], 'new_title': f'new_title_{uid}', 'new_description': None, 'new_price': None, 'new_currency': None, 'new_category_id': None}
    owner_username = {'owner_username': just_first_user['username']}

    r5 = client.post('/login', data={'username': just_second_user['username'], 'password': just_second_user['password']})
    assert r5.status_code == 200

    just_second_user_token = r5.json()['access_token']

    r6 = client.put(f'/products/{product_id}', json=updated_product, headers={'Authorization': f'Bearer {just_second_user_token}'})

    assert r6.status_code == 404

    r7 = client.request('DELETE', f'/products/{product_id}', json=owner_username, headers={'Authorization': f'Bearer {just_second_user_token}'})
    assert r7.status_code == 404













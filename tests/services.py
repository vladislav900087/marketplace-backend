import uuid
import secrets
import string
import random

class ServicesForTest:
    def generate_random_password(self, length=16):
        alphabet = string.ascii_letters + string.digits + string.punctuation

        return ''.join(secrets.choice(alphabet) for i in range(length))
    def create_random_user(self):
        uid = uuid.uuid4().hex[:8]
        password = self.generate_random_password()
        role = random.choice(('admin', 'user'))
        email = self.create_random_user_email()

        user = {'username': f'user_{uid}', 'password': password, 'role': role, 'email': email}
        return user

    def create_admin_user(self):
        uid = uuid.uuid4().hex[:8]
        password = self.generate_random_password()
        role = 'admin'
        email = self.create_random_user_email()

        user = {'username': f'user_{uid}', 'password': password, 'role': role, 'email': email}
        return user

    def create_user(self):
        uid = uuid.uuid4().hex[:8]
        password = self.generate_random_password()
        role = 'user'
        email = self.create_random_user_email()

        user = {'username': f'user_{uid}', 'password': password, 'role': role, 'email': email}

        return user

    def create_random_product(self):
        uid = uuid.uuid4().hex[:8]

        price = random.randint(1, 100)
        currency = random.choice(('EUR', 'USD', 'RUB', 'KZT'))

        product = {'title': f'product_{uid}', 'description': f'product_descr_{uid}',  'price': price, 'currency': currency, 'category_id': None}

        return product

    def create_random_user_email(self):
        uid = uuid.uuid4().hex[:8]

        return f'user_{uid}@gmail.com'
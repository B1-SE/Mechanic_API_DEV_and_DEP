import unittest
import json
from app import create_app
from app.extensions import db
from app.models import Customer

class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_customer_success(self):
        data = {"name": "John Doe", "email": "john@test.com", "password": "secret123"}
        response = self.client.post('/customers/', json=data)
        self.assertEqual(response.status_code, 201)

    def test_create_customer_missing_password(self):
        data = {"name": "John Doe", "email": "john@test.com"}
        response = self.client.post('/customers/', json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    def test_get_customer_not_found(self):
        response = self.client.get('/customers/999')
        self.assertEqual(response.status_code, 404)

    def test_update_customer_not_found(self):
        data = {"name": "Updated Name"}
        response = self.client.put('/customers/999', json=data)
        self.assertEqual(response.status_code, 404)

    def test_delete_customer_not_found(self):
        response = self.client.delete('/customers/999')
        self.assertEqual(response.status_code, 404)

    def test_login_invalid_credentials(self):
        data = {"email": "wrong@test.com", "password": "wrong"}
        response = self.client.post('/customers/login', json=data)
        self.assertEqual(response.status_code, 401)

    def test_my_tickets_no_token(self):
        response = self.client.get('/customers/my-tickets')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
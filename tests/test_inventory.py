import unittest
import json
from app import create_app
from app.extensions import db
from app.models import Inventory

class TestInventory(unittest.TestCase):
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

    def test_create_inventory_success(self):
        data = {"name": "Oil Filter", "price": 15.99}
        response = self.client.post('/inventory/', json=data)
        self.assertEqual(response.status_code, 201)

    def test_create_inventory_missing_fields(self):
        data = {"name": "Oil Filter"}
        response = self.client.post('/inventory/', json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)

    def test_get_inventory_item_not_found(self):
        response = self.client.get('/inventory/999')
        self.assertEqual(response.status_code, 404)

    def test_update_inventory_not_found(self):
        data = {"name": "Updated Filter", "price": 20.99}
        response = self.client.put('/inventory/999', json=data)
        self.assertEqual(response.status_code, 404)

    def test_delete_inventory_not_found(self):
        response = self.client.delete('/inventory/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
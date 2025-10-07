import unittest
import json
from app import create_app
from app.extensions import db
from app.models import Mechanic

class TestMechanics(unittest.TestCase):
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

    def test_create_mechanic_success(self):
        data = {"name": "Mike", "email": "mike@test.com", "specialization": "Engine", "experience": 5}
        response = self.client.post('/mechanics/', json=data)
        self.assertEqual(response.status_code, 201)

    def test_create_mechanic_missing_fields(self):
        data = {"name": "Mike"}
        response = self.client.post('/mechanics/', json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)

    def test_get_mechanic_not_found(self):
        response = self.client.get('/mechanics/999')
        self.assertEqual(response.status_code, 404)

    def test_update_mechanic_not_found(self):
        data = {"name": "Updated Name", "email": "updated@test.com", "specialization": "Brakes", "experience": 3}
        response = self.client.put('/mechanics/999', json=data)
        self.assertEqual(response.status_code, 404)

    def test_delete_mechanic_not_found(self):
        response = self.client.delete('/mechanics/999')
        self.assertEqual(response.status_code, 404)

    def test_get_mechanics_ranking(self):
        response = self.client.get('/mechanics/ranking')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
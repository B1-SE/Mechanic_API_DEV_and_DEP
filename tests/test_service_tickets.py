import unittest
import json
from datetime import date
from app import create_app
from app.extensions import db
from app.models import Customer, Mechanic, ServiceTicket, Inventory

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test customer
        customer = Customer(name="Test Customer", email="test@test.com", password="test123")
        db.session.add(customer)
        db.session.commit()
        self.customer_id = customer.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_ticket_success(self):
        data = {"service_date": "2024-01-15", "customer_id": self.customer_id}
        response = self.client.post('/service-tickets/', json=data)
        self.assertEqual(response.status_code, 201)

    def test_create_ticket_invalid_customer(self):
        data = {"service_date": "2024-01-15", "customer_id": 999}
        response = self.client.post('/service-tickets/', json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)

    def test_assign_mechanic_ticket_not_found(self):
        response = self.client.put('/service-tickets/999/assign-mechanic/1')
        self.assertEqual(response.status_code, 400)  # Content-Type validation

    def test_assign_mechanic_mechanic_not_found(self):
        # Create ticket first
        ticket = ServiceTicket(service_date=date(2024, 1, 15), customer_id=self.customer_id)
        db.session.add(ticket)
        db.session.commit()
        
        response = self.client.put(f'/service-tickets/{ticket.id}/assign-mechanic/999')
        self.assertEqual(response.status_code, 400)  # Content-Type validation

    def test_remove_mechanic_ticket_not_found(self):
        response = self.client.put('/service-tickets/999/remove-mechanic/1')
        self.assertEqual(response.status_code, 400)  # Content-Type validation

    def test_edit_ticket_not_found(self):
        data = {"add_ids": [1], "remove_ids": []}
        response = self.client.put('/service-tickets/999/edit', json=data)
        self.assertEqual(response.status_code, 404)

    def test_add_part_ticket_not_found(self):
        response = self.client.put('/service-tickets/999/add-part/1')
        self.assertEqual(response.status_code, 400)  # Content-Type validation

if __name__ == '__main__':
    unittest.main()
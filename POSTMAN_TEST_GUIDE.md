# Mechanic API - Postman Testing Guide

Base URL: `http://127.0.0.1:5000`

## Headers Required
For all POST/PUT requests:
- `Content-Type: application/json`

## 1. CUSTOMER ENDPOINTS

### Create Customer
- **Method**: POST
- **URL**: `{{base_url}}/customers/`
- **Body** (JSON):
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secret123",
  "dob": "1990-05-15"
}
```

### Get All Customers
- **Method**: GET
- **URL**: `{{base_url}}/customers/`

### Get Customer by ID
- **Method**: GET
- **URL**: `{{base_url}}/customers/1`

### Update Customer
- **Method**: PUT
- **URL**: `{{base_url}}/customers/1`
- **Body** (JSON):
```json
{
  "name": "John Smith",
  "email": "johnsmith@example.com"
}
```

### Delete Customer
- **Method**: DELETE
- **URL**: `{{base_url}}/customers/1`

## 2. MECHANIC ENDPOINTS

### Create Mechanic
- **Method**: POST
- **URL**: `{{base_url}}/mechanics/`
- **Body** (JSON):
```json
{
  "name": "Mike Johnson",
  "email": "mike@garage.com",
  "specialization": "Engine Repair",
  "experience": 5
}
```

### Get All Mechanics
- **Method**: GET
- **URL**: `{{base_url}}/mechanics/`

### Get Mechanic by ID
- **Method**: GET
- **URL**: `{{base_url}}/mechanics/1`

### Update Mechanic
- **Method**: PUT
- **URL**: `{{base_url}}/mechanics/1`
- **Body** (JSON):
```json
{
  "name": "Mike Johnson",
  "email": "mike@garage.com",
  "specialization": "Engine Repair",
  "experience": 5
}
```

### Delete Mechanic
- **Method**: DELETE
- **URL**: `{{base_url}}/mechanics/1`

## 3. SERVICE TICKET ENDPOINTS

### Create Service Ticket
- **Method**: POST
- **URL**: `{{base_url}}/service-tickets/`
- **Body** (JSON):
```json
POST /service-tickets/
{
  "service_date": "2024-01-15",
  "customer_id": 1
}
```

### Get All Service Tickets
- **Method**: GET
- **URL**: `{{base_url}}/service-tickets/`

### Assign Mechanic to Ticket
- **Method**: PUT
- **URL**: `{{base_url}}/service-tickets/1/assign-mechanic/1`

### Remove Mechanic from Ticket
- **Method**: PUT
- **URL**: `{{base_url}}/service-tickets/1/remove-mechanic/1`

## 4. TESTING SEQUENCE

1. **Create Customer** (save ID from response)
2. **Create Mechanic** (save ID from response)
3. **Create Service Ticket** (use customer ID)
4. **Assign Mechanic** to ticket
5. **Get All Service Tickets** (verify assignment)
6. **Remove Mechanic** from ticket
7. **Test all GET endpoints**
8. **Test UPDATE endpoints**
9. **Test DELETE endpoints**

## 5. POSTMAN ENVIRONMENT VARIABLES

Create environment with:
- `base_url`: `http://127.0.0.1:5000`

## 6. EXPECTED RESPONSES

### Success Responses:
- **201**: Created (POST requests)
- **200**: OK (GET, PUT, DELETE requests)

### Error Responses:
- **400**: Bad Request (validation errors)
- **404**: Not Found (resource doesn't exist)
- **415**: Unsupported Media Type (missing Content-Type)

## 7. COMMON ERRORS TO TEST

### Missing Content-Type
- Remove `Content-Type: application/json` header
- Expected: 400 error

### Invalid JSON
- Send malformed JSON
- Expected: 400 error

### Non-existent Resource
- Try GET/PUT/DELETE with ID 999
- Expected: 404 error

### Duplicate Email
- Create customer with same email twice
- Expected: 400 error
# Complete Mechanic API Test Guide

## 📦 Import Collection
Import `postman_collection_complete.json` into Postman

## 🔧 Setup Environment
Create environment with:
- `base_url`: `http://127.0.0.1:5001`

## 🚀 Automated Testing Suite

### **Collection Features:**
- **25 Total Requests** covering every endpoint
- **Automated variable management** (IDs stored automatically)
- **Built-in test assertions** for status codes
- **Sequential execution** with proper dependencies
- **Error testing** for edge cases

### **Test Sequence:**

#### **1. Health Check (1 request)**
- ✅ `GET /` - API status check

#### **2. Customers (6 requests)**
- ✅ `POST /customers/` - Create customer (saves ID)
- ✅ `GET /customers/` - Get all customers with pagination
- ✅ `GET /customers/{id}` - Get customer by ID
- ✅ `PUT /customers/{id}` - Update customer
- ✅ `POST /customers/login` - Login (saves token)
- ✅ `GET /customers/my-tickets` - Protected route with token

#### **3. Mechanics (5 requests)**
- ✅ `POST /mechanics/` - Create mechanic (saves ID)
- ✅ `GET /mechanics/` - Get all mechanics
- ✅ `GET /mechanics/{id}` - Get mechanic by ID
- ✅ `PUT /mechanics/{id}` - Update mechanic
- ✅ `GET /mechanics/ranking` - Get mechanics by ticket count

#### **4. Inventory (4 requests)**
- ✅ `POST /inventory/` - Create inventory item (saves ID)
- ✅ `GET /inventory/` - Get all inventory
- ✅ `GET /inventory/{id}` - Get inventory item by ID
- ✅ `PUT /inventory/{id}` - Update inventory item

#### **5. Service Tickets (6 requests)**
- ✅ `POST /service-tickets/` - Create service ticket (saves ID)
- ✅ `GET /service-tickets/` - Get all service tickets
- ✅ `PUT /service-tickets/{id}/assign-mechanic/{mechanic_id}` - Assign mechanic
- ✅ `PUT /service-tickets/{id}/add-part/{inventory_id}` - Add inventory part
- ✅ `PUT /service-tickets/{id}/edit` - Bulk edit mechanics
- ✅ `PUT /service-tickets/{id}/remove-mechanic/{mechanic_id}` - Remove mechanic

#### **6. Error Testing (4 requests)**
- ✅ `GET /customers/999` - Test 404 error
- ✅ `POST /customers/` (missing password) - Test 400 error
- ✅ `POST /customers/login` (invalid credentials) - Test 401 error
- ✅ `GET /customers/my-tickets` (no token) - Test 401 error

#### **7. Cleanup (3 requests)**
- ✅ `DELETE /customers/{id}` - Delete customer
- ✅ `DELETE /mechanics/{id}` - Delete mechanic
- ✅ `DELETE /inventory/{id}` - Delete inventory item

## 🎯 Running Tests

### **Option 1: Run Entire Collection**
1. Click "Run Collection" in Postman
2. Select all requests
3. Click "Run Mechanic API - Complete Test Suite"
4. View automated test results

### **Option 2: Run Individual Folders**
- Run each folder sequentially for focused testing
- Variables are automatically managed between requests

### **Option 3: Manual Testing**
- Execute requests individually
- Check response data and status codes
- Verify variable population

## 📊 Expected Results

### **Success Criteria:**
- ✅ All 25 requests execute successfully
- ✅ All automated tests pass (status code assertions)
- ✅ Variables populate correctly (customer_id, mechanic_id, etc.)
- ✅ Authentication token works for protected routes
- ✅ Relationships work (mechanic assignment, inventory parts)

### **Test Coverage:**
- **CRUD Operations**: Create, Read, Update, Delete for all resources
- **Authentication**: Login and protected route access
- **Relationships**: Mechanic-ticket and inventory-ticket associations
- **Advanced Features**: Pagination, ranking, bulk operations
- **Error Handling**: 400, 401, 404 error responses
- **Rate Limiting**: Requests respect configured limits

## 🔍 Validation Points

### **Data Integrity:**
- Customer creation with email validation
- Mechanic assignment to service tickets
- Inventory parts added to tickets
- Proper foreign key relationships

### **Security:**
- JWT token generation and validation
- Protected route access control
- Input validation and sanitization

### **Performance:**
- Caching on GET requests
- Rate limiting enforcement
- Pagination functionality

## 📝 Notes

- **Sequential Execution**: Run requests in order for proper variable management
- **Environment Variables**: Ensure base_url is set correctly
- **Token Expiry**: JWT tokens expire in 24 hours
- **Database**: Uses SQLite for easy testing
- **Rate Limits**: May need to wait between requests if limits are hit

## 🎉 Complete API Coverage

This collection tests **100% of your API endpoints** with:
- All 25 routes documented and tested
- Automated assertions for success/failure
- Variable management for seamless testing
- Error case validation
- Complete workflow testing

Perfect for development, CI/CD, and API validation!
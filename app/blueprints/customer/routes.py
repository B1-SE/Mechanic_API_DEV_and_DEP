from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, ServiceTicket, db
from . import customer_bp
from app.extensions import limiter, cache
from app.auth import encode_token, token_required

#Create CUSTOMER (POST)
#This endpoint creates a new user by deserializing and validating the incoming data.
#POST /customers Endpoint:
@customer_bp.route("/", methods=['POST'])
@limiter.limit("5 per day")
def create_customer():
    """
    Create a new customer
    ---
    tags:
      - Customers
    summary: Create a new customer
    description: Creates a new customer account with email validation
    parameters:
      - in: body
        name: customer
        description: Customer data
        required: true
        schema:
          $ref: '#/definitions/CustomerInput'
    responses:
      201:
        description: Customer created successfully
        schema:
          $ref: '#/definitions/Customer'
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
    """
    if not request.json or 'password' not in request.json:
        return jsonify({"password": ["Missing data for required field."]}), 400
        
    try:
        new_customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check if email already exists
    query = select(Customer).where(Customer.email == new_customer.email)
    existing_customer = db.session.execute(query).scalars().first()
    if existing_customer:
        return jsonify({"error": "Email already associated with an account."}), 400

    db.session.add(new_customer)
    db.session.commit()
    
    return customer_schema.jsonify(new_customer), 201

#RETRIEVE ALL CUSTOMERS (GET)
#When this request is received a function to retrieve and return all Customers will fire .
#GET /customers Endpoint:
@customer_bp.route("/", methods=['GET'])
@cache.cached(timeout=30)
@limiter.limit("3 per hour")
def get_customers():
    """
    Get all customers with pagination
    ---
    tags:
      - Customers
    summary: Retrieve all customers
    description: Returns paginated list of customers
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 10
    responses:
      200:
        description: List of customers
    """
    if request.headers.get('Accept') == 'text/html' or 'text/html' in request.headers.get('Accept', ''):
        from flask import Response
        html = '''<!DOCTYPE html>
<html><head><title>Customers API</title></head>
<body>
<h1>Customers API Endpoint</h1>
<p>This is a JSON API endpoint. Use tools like Postman or curl to interact with it.</p>
<p><a href="/">← Back to Home</a> | <a href="/docs">API Documentation</a></p>
</body></html>'''
        return Response(html, mimetype='text/html')
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    customers = db.session.query(Customer).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'customers': customers_schema.dump(customers.items),
        'total': customers.total,
        'pages': customers.pages,
        'current_page': customers.page,
        'per_page': customers.per_page
    }), 200

#RETRIEVE SPECIFIC CUSTOMER (GET)
#This endpoint includes a path parameter, which is a variable piece of the endpoint that can be used to pass information to the backend without sending a json body.
#GET /customers/{id} Endpoint:
@customer_bp.route("/<int:id>", methods=['GET'])
def get_customer(id):
    """
    Get customer by ID
    ---
    tags:
      - Customers
    summary: Get a specific customer
    description: Returns customer details by ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Customer details
        schema:
          $ref: '#/definitions/Customer'
      404:
        description: Customer not found
        schema:
          $ref: '#/definitions/Error'
    """
    customer = db.session.get(Customer, id)
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404

#UPDATE SPECIFIC CUSTOMER (PUT)
#This endpoint updates a customer’s information using their ID.
#PUT /customers/<id> Endpoint:
@customer_bp.route("/<int:id>", methods=['PUT'])
@limiter.limit("5 per month")
def update_customer(id):
    """
    Update customer
    ---
    tags:
      - Customers
    summary: Update customer information
    description: Updates customer details by ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: customer
        schema:
          $ref: '#/definitions/CustomerInput'
    responses:
      200:
        description: Customer updated
        schema:
          $ref: '#/definitions/Customer'
      404:
        description: Customer not found
        schema:
          $ref: '#/definitions/Error'
    """
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    try:
        customer_data = customer_schema.load(request.json, instance=customer)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return customer_schema.jsonify(customer_data), 200

#DELETE SPECIFIC CUSTOMER (DELETE)
#This endpoint deletes a customer by their ID.
#DELETE /customers/<id> Endpoint:
@customer_bp.route("/<int:id>", methods=['DELETE'])
@limiter.limit("5 per day")
def delete_customer(id):
    """
    Delete customer
    ---
    tags:
      - Customers
    summary: Delete a customer
    description: Deletes customer by ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Customer deleted
      404:
        description: Customer not found
        schema:
          $ref: '#/definitions/Error'
    """
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Customer id: {id}, successfully deleted.'}), 200

@customer_bp.route('/login', methods=['POST'])
def login():
    """
    Customer login
    ---
    tags:
      - Authentication
    summary: Login customer
    description: Authenticate customer and return JWT token
    parameters:
      - in: body
        name: credentials
        schema:
          $ref: '#/definitions/LoginInput'
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            token:
              type: string
      401:
        description: Invalid credentials
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        login_data = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == login_data['email'])
    customer = db.session.execute(query).scalars().first()
    
    if not customer or customer.password != login_data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = encode_token(customer.id)
    return jsonify({'token': token}), 200

@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    """
    Get customer's service tickets
    ---
    tags:
      - Customers
    summary: Get my service tickets
    description: Returns service tickets for authenticated customer
    security:
      - Bearer: []
    responses:
      200:
        description: List of service tickets
        schema:
          type: array
          items:
            $ref: '#/definitions/ServiceTicket'
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/Error'
    """
    from app.blueprints.service_ticket.schemas import service_tickets_schema
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200
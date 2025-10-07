from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db
from . import customer_bp
from app.extensions import limiter, cache

#Create CUSTOMER (POST)
#This endpoint creates a new user by deserializing and validating the incoming data.
#POST /customers Endpoint:
@customer_bp.route("/", methods=['POST'])
@limiter.limit("5 per day")
def create_customer():
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
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200

#RETRIEVE SPECIFIC CUSTOMER (GET)
#This endpoint includes a path parameter, which is a variable piece of the endpoint that can be used to pass information to the backend without sending a json body.
#GET /customers/{id} Endpoint:
@customer_bp.route("/<int:id>", methods=['GET'])
def get_customer(id):
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
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Customer id: {id}, successfully deleted.'}), 200
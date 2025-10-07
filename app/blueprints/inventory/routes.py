from flask import request, jsonify
from . import inventory_bp
from app.models import Inventory
from app.extensions import db, limiter, cache
from .schemas import inventory_schema, inventories_schema
from marshmallow import ValidationError

@inventory_bp.route('/', methods=['POST'])
@limiter.limit('10/day')
def create_inventory():
    """
    Create a new inventory item
    ---
    tags:
      - Inventory
    summary: Create a new inventory item
    description: Adds a new part to inventory
    parameters:
      - in: body
        name: inventory
        schema:
          $ref: '#/definitions/InventoryInput'
    responses:
      201:
        description: Inventory item created
        schema:
          $ref: '#/definitions/Inventory'
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        item = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(item)
    db.session.commit()
    return inventory_schema.jsonify(item), 201

@inventory_bp.route('/', methods=['GET'])
@cache.cached(timeout=30)
def get_inventory():
    """
    Get all inventory items
    ---
    tags:
      - Inventory
    summary: Retrieve all inventory items
    description: Returns list of all inventory items
    responses:
      200:
        description: List of inventory items
        schema:
          type: array
          items:
            $ref: '#/definitions/Inventory'
    """
    from flask import request
    if request.headers.get('Accept') == 'text/html' or 'text/html' in request.headers.get('Accept', ''):
        from flask import Response
        html = '''<!DOCTYPE html>
<html><head><title>Inventory API</title></head>
<body>
<h1>Inventory API Endpoint</h1>
<p>This is a JSON API endpoint. Use tools like Postman or curl to interact with it.</p>
<p><a href="/">← Back to Home</a> | <a href="/docs">API Documentation</a></p>
</body></html>'''
        return Response(html, mimetype='text/html')
    items = db.session.query(Inventory).all()
    return inventories_schema.jsonify(items), 200

@inventory_bp.route('/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_inventory_item(id):
    """
    Get inventory item by ID
    ---
    tags:
      - Inventory
    summary: Get a specific inventory item
    description: Returns inventory item details by ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Inventory item details
        schema:
          $ref: '#/definitions/Inventory'
      404:
        description: Inventory item not found
        schema:
          $ref: '#/definitions/Error'
    """
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({"error": "Inventory item not found"}), 404
    return inventory_schema.jsonify(item), 200

@inventory_bp.route('/<int:id>', methods=['PUT'])
@limiter.limit('10/month')
def update_inventory(id):
    """
    Update inventory item
    ---
    tags:
      - Inventory
    summary: Update inventory item information
    description: Updates inventory item details by ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: inventory
        schema:
          $ref: '#/definitions/InventoryInput'
    responses:
      200:
        description: Inventory item updated
        schema:
          $ref: '#/definitions/Inventory'
      404:
        description: Inventory item not found
        schema:
          $ref: '#/definitions/Error'
    """
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({"error": "Inventory item not found"}), 404
    try:
        updated_item = inventory_schema.load(request.json, instance=item)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.commit()
    return inventory_schema.jsonify(updated_item), 200

@inventory_bp.route('/<int:id>', methods=['DELETE'])
@limiter.limit('10/day')
def delete_inventory(id):
    """
    Delete inventory item
    ---
    tags:
      - Inventory
    summary: Delete an inventory item
    description: Deletes inventory item by ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Inventory item deleted
      404:
        description: Inventory item not found
        schema:
          $ref: '#/definitions/Error'
    """
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({"error": "Inventory item not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Inventory item id: {id}, successfully deleted."}), 200
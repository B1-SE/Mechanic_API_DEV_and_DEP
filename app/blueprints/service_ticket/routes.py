from flask import request, jsonify
from . import service_ticket_bp
from app.models import ServiceTicket, Mechanic, Inventory
from app.extensions import db, limiter, cache
from .schemas import service_ticket_schema, service_tickets_schema
from marshmallow import ValidationError

@service_ticket_bp.route('/', methods=['POST'])
@limiter.limit('20/day')
def create_ticket():
    """
    Create a new service ticket
    ---
    tags:
      - Service Tickets
    summary: Create a new service ticket
    description: Creates a new service ticket for a customer
    parameters:
      - in: body
        name: ticket
        schema:
          $ref: '#/definitions/ServiceTicketInput'
    responses:
      201:
        description: Service ticket created
        schema:
          $ref: '#/definitions/ServiceTicket'
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        ticket = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if customer exists
    from app.models import Customer
    customer = db.session.get(Customer, ticket.customer_id)
    if not customer:
        return jsonify({"error": f"Customer with id {ticket.customer_id} not found"}), 400
    
    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 201

@service_ticket_bp.route('/', methods=['GET'])
@cache.cached(timeout=30)
def get_tickets():
    """
    Get all service tickets
    ---
    tags:
      - Service Tickets
    summary: Retrieve all service tickets
    description: Returns list of all service tickets
    responses:
      200:
        description: List of service tickets
        schema:
          type: array
          items:
            $ref: '#/definitions/ServiceTicket'
    """
    from flask import request
    if request.headers.get('Accept') == 'text/html' or 'text/html' in request.headers.get('Accept', ''):
        from flask import Response
        html = '''<!DOCTYPE html>
<html><head><title>Service Tickets API</title></head>
<body>
<h1>Service Tickets API Endpoint</h1>
<p>This is a JSON API endpoint. Use tools like Postman or curl to interact with it.</p>
<p><a href="/">← Back to Home</a> | <a href="/docs">API Documentation</a></p>
</body></html>'''
        return Response(html, mimetype='text/html')
    tickets = db.session.query(ServiceTicket).all()
    return service_tickets_schema.jsonify(tickets), 200

@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    """
    Assign mechanic to ticket
    ---
    tags:
      - Service Tickets
    summary: Assign a mechanic to a service ticket
    description: Creates relationship between mechanic and service ticket
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: path
        name: mechanic_id
        type: integer
        required: true
    responses:
      200:
        description: Mechanic assigned
        schema:
          $ref: '#/definitions/ServiceTicket'
      404:
        description: Ticket or mechanic not found
        schema:
          $ref: '#/definitions/Error'
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    if mech not in ticket.mechanics:
        ticket.mechanics.append(mech)
        db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    """
    Remove mechanic from ticket
    ---
    tags:
      - Service Tickets
    summary: Remove a mechanic from a service ticket
    description: Removes relationship between mechanic and service ticket
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: path
        name: mechanic_id
        type: integer
        required: true
    responses:
      200:
        description: Mechanic removed
        schema:
          $ref: '#/definitions/ServiceTicket'
      404:
        description: Ticket or mechanic not found
        schema:
          $ref: '#/definitions/Error'
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    if mech in ticket.mechanics:
        ticket.mechanics.remove(mech)
        db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_ticket_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    """
    Edit ticket mechanics
    ---
    tags:
      - Service Tickets
    summary: Add/remove multiple mechanics from ticket
    description: Bulk add or remove mechanics from service ticket
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: body
        name: mechanics
        schema:
          type: object
          properties:
            add_ids:
              type: array
              items:
                type: integer
            remove_ids:
              type: array
              items:
                type: integer
    responses:
      200:
        description: Ticket updated
        schema:
          $ref: '#/definitions/ServiceTicket'
      404:
        description: Ticket not found
        schema:
          $ref: '#/definitions/Error'
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    
    data = request.get_json() or {}
    remove_ids = data.get('remove_ids', [])
    add_ids = data.get('add_ids', [])
    
    for mid in remove_ids:
        mech = db.session.get(Mechanic, mid)
        if mech and mech in ticket.mechanics:
            ticket.mechanics.remove(mech)
    
    for mid in add_ids:
        mech = db.session.get(Mechanic, mid)
        if mech and mech not in ticket.mechanics:
            ticket.mechanics.append(mech)
    
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_ticket_bp.route('/<int:ticket_id>/add-part/<int:inventory_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, inventory_id):
    """
    Add inventory part to ticket
    ---
    tags:
      - Service Tickets
    summary: Add inventory part to service ticket
    description: Associates an inventory item with a service ticket
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: path
        name: inventory_id
        type: integer
        required: true
    responses:
      200:
        description: Part added to ticket
        schema:
          $ref: '#/definitions/ServiceTicket'
      404:
        description: Ticket or inventory item not found
        schema:
          $ref: '#/definitions/Error'
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    
    part = db.session.get(Inventory, inventory_id)
    if not part:
        return jsonify({"error": "Inventory item not found"}), 404
    
    if part not in ticket.inventory:
        ticket.inventory.append(part)
        db.session.commit()
    
    return service_ticket_schema.jsonify(ticket), 200
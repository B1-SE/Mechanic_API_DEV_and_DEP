from flask import request, jsonify
from . import service_ticket_bp
from app.models import ServiceTicket, Mechanic
from app.extensions import db, limiter, cache
from .schemas import service_ticket_schema, service_tickets_schema
from marshmallow import ValidationError

@service_ticket_bp.route('/', methods=['POST'])
@limiter.limit('20/day')
def create_ticket():
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
    tickets = db.session.query(ServiceTicket).all()
    return service_tickets_schema.jsonify(tickets), 200

@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
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
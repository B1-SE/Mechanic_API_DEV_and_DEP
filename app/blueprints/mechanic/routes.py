from flask import request, jsonify
from app.blueprints.mechanic import mechanic_bp
from app.extensions import db, limiter, cache
from app.models import Mechanic
from .schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError

@mechanic_bp.route('/', methods=['POST'])
@limiter.limit('10/day')
def create_mechanic():
    payload = request.get_json() or {}
    try:
        mech = mechanic_schema.load(payload)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(mech)
    db.session.commit()
    return mechanic_schema.jsonify(mech), 201

@mechanic_bp.route('/', methods=['GET'])
@cache.cached(timeout=30)
def get_mechanics():
    mechs = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechs), 200

@mechanic_bp.route('/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_mechanic(id):
    mech = db.session.get(Mechanic, id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mech), 200

@mechanic_bp.route('/<int:id>', methods=['PUT'])
@limiter.limit('10/month')
def update_mechanic(id):
    mech = db.session.get(Mechanic, id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    try:
        updated_mech = mechanic_schema.load(request.json, instance=mech)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.commit()
    return mechanic_schema.jsonify(updated_mech), 200

@mechanic_bp.route('/<int:id>', methods=['DELETE'])
@limiter.limit('10/day')
def delete_mechanic(id):
    mech = db.session.get(Mechanic, id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"Mechanic id: {id}, successfully deleted."}), 200


from flask import request, jsonify
from app.blueprints.mechanic import mechanic_bp
from app.extensions import db, limiter, cache
from app.models import Mechanic
from .schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError

@mechanic_bp.route('/', methods=['POST'])
@limiter.limit('10/day')
def create_mechanic():
    """
    Create a new mechanic
    ---
    tags:
      - Mechanics
    summary: Create a new mechanic
    description: Creates a new mechanic profile
    parameters:
      - in: body
        name: mechanic
        schema:
          $ref: '#/definitions/MechanicInput'
    responses:
      201:
        description: Mechanic created
        schema:
          $ref: '#/definitions/Mechanic'
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
    """
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
    """
    Get all mechanics
    ---
    tags:
      - Mechanics
    summary: Retrieve all mechanics
    description: Returns list of all mechanics
    responses:
      200:
        description: List of mechanics
        schema:
          type: array
          items:
            $ref: '#/definitions/Mechanic'
    """
    from flask import request
    if request.headers.get('Accept') == 'text/html' or 'text/html' in request.headers.get('Accept', ''):
        from flask import Response
        html = '''<!DOCTYPE html>
<html><head><title>Mechanics API</title></head>
<body>
<h1>Mechanics API Endpoint</h1>
<p>This is a JSON API endpoint. Use tools like Postman or curl to interact with it.</p>
<p><a href="/">← Back to Home</a> | <a href="/docs">API Documentation</a></p>
</body></html>'''
        return Response(html, mimetype='text/html')
    mechs = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechs), 200

@mechanic_bp.route('/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_mechanic(id):
    """
    Get mechanic by ID
    ---
    tags:
      - Mechanics
    summary: Get a specific mechanic
    description: Returns mechanic details by ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Mechanic details
        schema:
          $ref: '#/definitions/Mechanic'
      404:
        description: Mechanic not found
        schema:
          $ref: '#/definitions/Error'
    """
    mech = db.session.get(Mechanic, id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mech), 200

@mechanic_bp.route('/<int:id>', methods=['PUT'])
@limiter.limit('10/month')
def update_mechanic(id):
    """
    Update mechanic
    ---
    tags:
      - Mechanics
    summary: Update mechanic information
    description: Updates mechanic details by ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: mechanic
        schema:
          $ref: '#/definitions/MechanicInput'
    responses:
      200:
        description: Mechanic updated
        schema:
          $ref: '#/definitions/Mechanic'
      404:
        description: Mechanic not found
        schema:
          $ref: '#/definitions/Error'
    """
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
    """
    Delete mechanic
    ---
    tags:
      - Mechanics
    summary: Delete a mechanic
    description: Deletes mechanic by ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Mechanic deleted
      404:
        description: Mechanic not found
        schema:
          $ref: '#/definitions/Error'
    """
    mech = db.session.get(Mechanic, id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"Mechanic id: {id}, successfully deleted."}), 200

@mechanic_bp.route('/ranking', methods=['GET'])
@cache.cached(timeout=60)
def get_mechanics_by_tickets():
    """
    Get mechanics ranked by ticket count
    ---
    tags:
      - Mechanics
    summary: Get mechanics ranking
    description: Returns mechanics ordered by number of tickets worked on
    responses:
      200:
        description: Ranked list of mechanics
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
              specialization:
                type: string
              experience:
                type: integer
              ticket_count:
                type: integer
    """
    from sqlalchemy import func
    from app.models import Service_Mechanic
    
    # Query mechanics ordered by ticket count
    mechanics_with_counts = db.session.query(
        Mechanic,
        func.count(Service_Mechanic.c.service_ticket_id).label('ticket_count')
    ).outerjoin(Service_Mechanic).group_by(Mechanic.id).order_by(
        func.count(Service_Mechanic.c.service_ticket_id).desc()
    ).all()
    
    result = []
    for mech, count in mechanics_with_counts:
        mech_data = mechanic_schema.dump(mech)
        mech_data['ticket_count'] = count
        result.append(mech_data)
    
    return jsonify(result), 200


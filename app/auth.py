from functools import wraps
from flask import request, jsonify, current_app
from jose import jwt, JWTError
import datetime

def encode_token(customer_id):
    payload = {
        'customer_id': customer_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config.get('SECRET_KEY', 'dev-secret'), algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY', 'dev-secret'), algorithms=['HS256'])
            customer_id = payload['customer_id']
        except JWTError:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(customer_id, *args, **kwargs)
    return decorated
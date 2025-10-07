from flask import Flask
from .extensions import ma, limiter, cache, db
from .blueprints.customer import customer_bp
from .blueprints.mechanic import mechanic_bp
from .blueprints.service_ticket import service_ticket_bp

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    # Initialize extensions here (e.g., db, ma)
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    @app.before_request
    def check_content_type():
        from flask import request, jsonify
        if request.method in ['POST', 'PUT'] and request.content_type != 'application/json':
            return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    # Register Blueprints and set url prefixes (plural names)
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')

    # Simple root / health-check route
    @app.route('/')
    def index():
        return {'status': 'ok', 'routes': ['/customers', '/mechanics', '/service-tickets']}, 200
    
    @app.errorhandler(404)
    def not_found(error):
        from flask import jsonify
        return jsonify({
            'error': 'Route not found',
            'available_routes': ['/customers', '/mechanics', '/service-tickets']
        }), 404
    
    return app
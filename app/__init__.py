from flask import Flask
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from .extensions import ma, limiter, cache, db
from .blueprints.customer import customer_bp
from .blueprints.mechanic import mechanic_bp
from .blueprints.service_ticket import service_ticket_bp
from .blueprints.inventory import inventory_bp
from .swagger_config import swagger_config

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
        if request.method in ['POST', 'PUT'] and request.data and not request.content_type:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    # Register Blueprints and set url prefixes (plural names)
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    
    # Swagger UI setup
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint)

    # Simple root / health-check route
    @app.route('/')
    def index():
        return {'status': 'ok', 'routes': ['/customers', '/mechanics', '/service-tickets', '/inventory'], 'docs': '/docs'}, 200
    
    @app.route('/swagger.json')
    def swagger_spec():
        return swagger_config
    
    @app.errorhandler(404)
    def not_found(error):
        from flask import jsonify
        return jsonify({
            'error': 'Route not found',
            'available_routes': ['/customers', '/mechanics', '/service-tickets', '/inventory']
        }), 404
    
    return app
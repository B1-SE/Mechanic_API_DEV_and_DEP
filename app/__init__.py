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
        from flask import Response
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mechanic Shop API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .endpoints { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 30px 0; }
        .endpoint { background: #007bff; color: white; padding: 15px; border-radius: 5px; text-align: center; text-decoration: none; }
        .endpoint:hover { background: #0056b3; }
        .docs-link { background: #28a745; display: block; text-align: center; padding: 15px; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }
        .docs-link:hover { background: #1e7e34; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Mechanic Shop API</h1>
        <p style="text-align: center; color: #666;">RESTful API for managing customers, mechanics, service tickets, and inventory</p>
        
        <div class="endpoints">
            <a href="/customers/" class="endpoint">👥 Customers</a>
            <a href="/mechanics/" class="endpoint">🔧 Mechanics</a>
            <a href="/service-tickets/" class="endpoint">🎫 Service Tickets</a>
            <a href="/inventory/" class="endpoint">📦 Inventory</a>
        </div>
        
        <a href="/docs" class="docs-link">📚 API Documentation (Swagger)</a>
        
        <div style="text-align: center; margin-top: 30px; color: #666; font-size: 14px;">
            <p>Status: ✅ Online | Environment: Production</p>
        </div>
    </div>
</body>
</html>'''
        return Response(html, mimetype='text/html')
    
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
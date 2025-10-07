from app import create_app
from app.extensions import db
import os
import logging

# Load environment variables from .env file (development only)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available in production

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Use ProductionConfig for deployment
    config_name = 'ProductionConfig' if os.environ.get('FLASK_ENV') == 'production' else 'DevelopmentConfig'
    app = create_app(config_name)
    logger.info(f"Flask app created successfully with {config_name}")
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error during app initialization: {str(e)}")
    # Fallback to development config
    try:
        app = create_app('DevelopmentConfig')
        logger.info("Fallback to DevelopmentConfig successful")
    except Exception as fallback_error:
        logger.error(f"Fallback failed: {str(fallback_error)}")
        raise

# For development only
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=False)
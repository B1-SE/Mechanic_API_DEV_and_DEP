from app import create_app
from app.extensions import db
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use ProductionConfig for deployment
app = create_app('ProductionConfig')

# Create database tables
with app.app_context():
    db.create_all()

# For development only
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=False)
from . import create_app
from .extensions import db

def main():
    app = create_app('DevelopmentConfig')
    with app.app_context():
        db.create_all()
    app.run()

if __name__ == "__main__":
    main()
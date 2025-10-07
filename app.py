from app import create_app
from app.extensions import db
import os

app = create_app('DevelopmentConfig')

def main():
    port = int(os.environ.get("PORT", 5000))
    skip_db = os.environ.get("SKIP_DB_CREATE")
    no_reload = bool(os.environ.get("NO_RELOAD"))
    if not skip_db:
        with app.app_context():
            db.create_all()
    # when NO_RELOAD=1 we disable the auto-reloader to avoid fork/suspended-child issues
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=not no_reload)

if __name__ == "__main__":
    main()
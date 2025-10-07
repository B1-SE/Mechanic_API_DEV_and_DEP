from flask import Blueprint

mechanic_bp = Blueprint('mechanic_bp', __name__)

# import routes so decorators attach to blueprint
from . import routes  # noqa: F401,E402
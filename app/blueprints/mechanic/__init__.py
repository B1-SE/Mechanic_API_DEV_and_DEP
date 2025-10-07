from flask import Blueprint

mechanic_bp = Blueprint('mechanic', __name__)

# import routes so decorators attach to blueprint
from . import routes  # noqa: F401,E402
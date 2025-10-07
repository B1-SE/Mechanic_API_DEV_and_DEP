from flask import Blueprint

service_ticket_bp = Blueprint('service_ticket_bp', __name__)

# import routes so decorators attach to the blueprint
from . import routes  # noqa: F401,E402
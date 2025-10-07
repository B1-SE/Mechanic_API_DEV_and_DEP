from flask import Blueprint

# DO NOT set url_prefix here; register prefix in create_app
customer_bp = Blueprint('customer_bp', __name__)

from . import routes  # noqa: F401
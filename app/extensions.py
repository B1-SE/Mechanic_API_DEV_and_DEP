from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# singletons used across the app
db = SQLAlchemy()
ma = Marshmallow()
# In-memory limiter for dev; configure a storage backend for production
limiter = Limiter(key_func=get_remote_address, default_limits=[])
# SimpleCache for dev to silence CACHE_TYPE null warning
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
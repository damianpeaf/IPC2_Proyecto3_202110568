import imp
from flask import Flask

from .routes import default_routes

# Init app
app = Flask(__name__)

# Blueprint

app.register_blueprint(default_routes)

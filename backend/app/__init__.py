import imp
from flask import Flask
from .db.orm import Orm
from .routes import default_routes

# Init app
app = Flask(__name__)

# Blueprint

app.register_blueprint(default_routes)

# Init db
Orm.init()
Orm.save()


import imp
from flask import Flask
from .db.orm import Orm
from .routes import default_routes, report_routes

# Init app
app = Flask(__name__, static_folder='views/static', template_folder='views/templates')

# Blueprint

app.register_blueprint(default_routes)
app.register_blueprint(report_routes)

# Init db
Orm.init()
Orm.save()


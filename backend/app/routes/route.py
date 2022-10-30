from crypt import methods
from flask import Blueprint

default_routes = Blueprint("default", __name__)

@default_routes.route('/', methods=['GET'])
def default():
    return 'Hola mundo'
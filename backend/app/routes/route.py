from flask import Blueprint, jsonify, request
from ..controller import fetch_all_data, create_resource, create_category

default_routes = Blueprint("main", __name__)

@default_routes.route('/', methods=['GET'])
def default():
    return 'Tecnologías Chapinas, S.A API'

@default_routes.route('/consultarDatos', methods=['GET'])
def consult_data():
    return jsonify(fetch_all_data())

@default_routes.route('/crearRecurso', methods=['POST'])
def create_resource_():
    res = create_resource(request.json)
    return jsonify(res)

@default_routes.route('/crearCategoria', methods=['POST'])
def create_category_():
    res = create_category(request.json)
    return jsonify(res)
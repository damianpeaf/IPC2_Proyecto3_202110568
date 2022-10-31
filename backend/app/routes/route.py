from flask import Blueprint, jsonify, request

from ..controller import read_configuration_file,fetch_all_data, create_resource, create_category, create_configuration, create_client, create_instance, create_consumption

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

@default_routes.route('/crearConfiguracion', methods=['POST'])
def create_configuration_():
    res = create_configuration(request.json)
    return jsonify(res)

@default_routes.route('/crearCliente', methods=['POST'])
def create_client_():
    res = create_client(request.json)
    return jsonify(res)

@default_routes.route('/crearInstancia', methods=['POST'])
def create_instance_():
    res = create_instance(request.json)
    return jsonify(res)

@default_routes.route('/crearConsumo', methods=['POST'])
def create_consumption_():
    res = create_consumption(request.json)
    
    return jsonify(res)

@default_routes.route('/mensajeConfiguracion', methods=['POST'])
def configuration_message_():
    resp = read_configuration_file(request.files)
    return jsonify(resp)



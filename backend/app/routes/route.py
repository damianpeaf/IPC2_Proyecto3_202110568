from flask import Blueprint, jsonify, request

from ..controller import generate_bill,read_configuration_file,read_consumption_file,cancel_instance, fetch_all_data, create_resource, create_category, create_configuration, create_client, create_instance, create_consumption

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


@default_routes.route('/mensajeConsumo', methods=['POST'])
def consumption_file_():
    resp = read_consumption_file(request.files)
    return jsonify(resp)


@default_routes.route('/cancelarInstancia', methods=['POST'])
def cancel_instance_():
    resp = cancel_instance(request.json)
    return jsonify(resp)


@default_routes.route('/generarFactura', methods=['POST'])
def generate_bill_():
    resp = generate_bill(request.json)
    return jsonify(resp)


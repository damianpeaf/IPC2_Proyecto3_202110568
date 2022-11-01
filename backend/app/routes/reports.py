from flask import Blueprint, jsonify, request

from ..controller import category_report, resource_report
report_routes = Blueprint("reports", __name__, url_prefix="/reporte")

@report_routes.route('/factura', methods=['POST'])
def bill_report_():
    return 'Tecnologías Chapinas, S.A API'

@report_routes.route('/recurso', methods=['POST'])
def resource_report_():
    resp = resource_report(request.json)
    return resp

@report_routes.route('/categoria', methods=['POST'])
def category_report_():
    resp = category_report(request.json)
    return resp
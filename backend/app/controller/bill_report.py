

from typing import Dict
from flask import make_response, render_template, jsonify
import pdfkit

from ..utils import get_value
from ..db import Orm

def bill_report(fields :Dict):

    try:
        id_ = get_value(fields, 'id', str)


        bill =  Orm.searchById('bills', id_)

        if bill == None:
            raise Error('Factura no encontrada')

        rendered = render_template('bill_report.html', title='Reporte factura', total=str(bill.total), nit=bill.nit, date=bill.date, correlative=bill.id_, intances=bill.instance_detail, consumptions =bill.detail)
        pdf = pdfkit.from_string(rendered, False)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment;filename=report.pdf'
        return response
        
    except Exception as e:
        return jsonify({
            "msg": str(e)
        })

class Error(Exception):
    pass

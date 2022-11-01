

from typing import Dict
from flask import make_response, render_template, jsonify
import pdfkit

from ..utils import get_value, parse_to_datetime
from ..db import Orm

def resource_report(fields :Dict):

    try:
        from_ = parse_to_datetime(get_value(fields, 'from', str))
        to_ = parse_to_datetime(get_value(fields, 'to', str))

        if from_ == None or to_ == None:
            raise DateError('Formato de fecha incorrecto')

        if from_ > to_:
            raise DateError('La fecha de finalizacion tiene que ser mayor a la de inicio')


        report = {
            "resources": [],
        }

        # fill dict
        resources = Orm.tables['resources']
        for resource in resources:
            report['resources'].append({"name" :resource.name, "id": resource.id_, "revenue": 0})
        
        
        consumptions = Orm.tables['consumptions']
        for consumption in consumptions:

            date = parse_to_datetime(consumption.date)
            if date < from_ or date > to_ :
                continue

            hours = consumption.time
            configuration = Orm.searchById('instances', consumption.instance_id).configuration
            
            for detail in configuration.resources:
                total =  round(detail.quantity,2) * round(detail.resource.value_per_hour,2) * round(hours,2)

                for r in report['resources']:
                    if r["id"] == detail.resource.id_:
                        r['revenue']+= total
                        r['revenue'] =round(r['revenue'],2)

        rendered = render_template('resources_report.html', title='Reporte', resources=report['resources'])
        pdf = pdfkit.from_string(rendered, False)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment;filename=report.pdf'
        return response
        
    except Exception as e:
        return jsonify({
            "msg": str(e)
        })

class DateError(Exception):
    pass

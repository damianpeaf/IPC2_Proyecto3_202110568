from flask import jsonify,  make_response, render_template
from typing import Dict
import pdfkit

from ..utils import get_value, parse_to_datetime,calculate_total_price_of_configuration
from ..db import Orm


def category_report(fields :Dict):

    try:
        from_ = parse_to_datetime(get_value(fields, 'from', str))
        to_ = parse_to_datetime(get_value(fields, 'to', str))

        if from_ == None or to_ == None:
            raise DateError('Formato de fecha incorrecto')

        if from_ > to_:
            raise DateError('La fecha de finalizacion tiene que ser mayor a la de inicio')


        report = {
            "categories": [],
            "configurations": []
        }

        # fill dict
        categories = Orm.tables['categories']
        for category in categories:
            report['categories'].append({"name" :category.name, "id": category.id_, "revenue": 0})
        

        configurations = Orm.tables['configurations']
        for conf in configurations:
            report['configurations'].append({"name" :conf.name, "id": conf.id_, "revenue": 0})
        
        consumptions = Orm.tables['consumptions']
        for consumption in consumptions:

            date = parse_to_datetime(consumption.date)
            if date < from_ or date > to_ :
                continue

            hours = consumption.time
            configuration = Orm.searchById('instances', consumption.instance_id).configuration
            category = Orm.search_category_by_configuration(configuration.id_)
            total = calculate_total_price_of_configuration(configuration, hours)

            for c in report['categories']:
                if c["id"] == category.id_:
                    c['revenue']+= total
                    c['revenue'] =round(c['revenue'],2)

            for c in report['configurations']:
                if c["id"] == configuration.id_:
                    c['revenue']+= total
                    c['revenue'] =round(c['revenue'],2)


        rendered = render_template('categories_report.html', title='Reporte', categories=report['categories'], configurations=report['configurations'])
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

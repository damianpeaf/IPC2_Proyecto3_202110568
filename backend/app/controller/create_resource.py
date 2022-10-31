
from typing import Dict
from dataclasses import asdict

from ..models import Resource
from ..db import Orm
from ..utils import get_value

def create_resource(fields:Dict):
    try:
        id_ = get_value(fields, 'id', str)
        name = get_value(fields, 'name')
        abreviation = get_value(fields, 'abreviation', str)
        metric = get_value(fields, 'metric', str)
        type = get_value(fields, 'type', str)
        value_per_hour = float(get_value(fields, 'value_per_hour'))

        new_resource = Resource(id_, name, abreviation, metric, type, value_per_hour)

        Orm.create('resources', new_resource)
        Orm.save()

        return {
            'msg': 'Recurso creado exitosamente',
            'resource': asdict(new_resource)
        }

    except Exception as e:
        return {
            'msg': str(e)
        }


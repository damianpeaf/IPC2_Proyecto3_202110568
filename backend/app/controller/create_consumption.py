
from typing import Dict
from dataclasses import asdict

from ..models import Consumption
from ..db import Orm
from ..utils import get_value, eval_datetime_string

class AttributeNotFound(Exception):
    pass

def create_consumption(fields:Dict):
    try:
        nit = get_value(fields, 'nit', str)
        instance_id = get_value(fields, 'instance', str)
        time = float(get_value(fields, 'time'))
        date = eval_datetime_string(get_value(fields, 'date', str))

        if date == None:
            date_ = fields['date']
            raise AttributeNotFound(f'La fecha {date_} tiene el formato incorrecto')

        instance = Orm.searchById('instances', instance_id)

        if instance is None:
            raise AttributeNotFound(f'No se encontró la instancia con id {instance_id}')


        client = Orm.searchById('clients', nit)

        if client is None:
            raise AttributeNotFound(f'No se encontró el cliente con nit {nit}')

        new_consumption = Consumption(nit, instance_id, time, date)

        Orm.create('consumptions', new_consumption)
        instance.consumptions.append(new_consumption)

        Orm.save()

        return {
            'msg': 'Consumo creado exitosamente',
            'consumption': asdict(new_consumption)
        }

    except Exception as e:
        return {
            'msg': str(e)
        }


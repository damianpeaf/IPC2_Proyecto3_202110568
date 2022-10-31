
from typing import Dict
from dataclasses import asdict
from datetime import datetime

from ..models import Instance
from ..db import Orm
from ..utils import get_value

class AttributeNotFound(Exception):
    pass

def create_instance(fields:Dict):
    try:
        id_ = get_value(fields, 'id', str)
        name = get_value(fields, 'name', str)
        init_date = datetime.now().strftime("%d/%m/%Y")
        state = "Vigente"
        end_date = None
        consumptions = []
        configuration = get_value(fields, 'configuration', str)

        configuration_object = Orm.searchById('configurations', configuration)

        if configuration_object == None:
            raise AttributeNotFound('Configuracion no encontrada')

        new_instance = Instance(id_, configuration_object, name, init_date, state, end_date, consumptions)

        Orm.create('instances', new_instance)

        # * search for user

        nit = get_value(fields, 'nit', str)

        client = Orm.searchById('clients', nit)

        if client == None:
            raise AttributeNotFound(f"Cliente con nit {nit} no encntrado")

        client.instances.append(new_instance)

        Orm.save()

        return {
            'msg': 'Cliente creado exitosamente',
            'instance': asdict(new_instance)
        }

    except Exception as e:
        return {
            'msg': str(e)
        }



from typing import Dict
from dataclasses import asdict

from ..models import Category
from ..db import Orm
from ..utils import get_value

class ConfigurationNotFound(Exception):
    pass


def create_category(fields:Dict):
    try:
        id_ = get_value(fields, 'id', str)
        name = get_value(fields, 'name', str)
        description = get_value(fields, 'description', str)
        work_load = get_value(fields, 'work_load', str)
        configurations = get_value(fields, 'configurations', list)
        
        configurations_objects = []
        for configuration_id in configurations:
            conf = Orm.searchById('configurations',configuration_id)

            if conf == None:
                raise ConfigurationNotFound(f'No se encontró configuration con la id {configuration_id}')
            configurations_objects.append(conf)

        new_category = Category(id_, name, description, work_load, configurations_objects)

        Orm.create('categories', new_category)
        Orm.save()

        return {
            'msg': 'Categoria creado exitosamente',
            'category': asdict(new_category)
        }

    except Exception as e:
        return {
            'msg': str(e)
        }


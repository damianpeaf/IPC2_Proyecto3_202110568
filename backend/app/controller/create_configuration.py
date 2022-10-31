
from typing import Dict
from dataclasses import asdict

from ..models import Configuration, ResourceConfiguration
from ..db import Orm
from ..utils import get_value

class ResourceNotFound(Exception):
    pass

def create_configuration(fields:Dict):
    try:
        id_ = get_value(fields, 'id', str)
        name = get_value(fields, 'name', str)
        description = get_value(fields, 'description', str)
        resource_configurations = get_value(fields, 'resources', list)
        
        resources_configurations_objects = []
        for resource_configuration in resource_configurations:
            try:
                resource_id = resource_configuration[0]
                resource_quantity = float(resource_configuration[1])

                resource = Orm.searchById('resources',resource_id)

                if resource == None:
                    raise ResourceNotFound(f'No se encontró el recurso con la id {resource_id}')
                resources_configurations_objects.append(ResourceConfiguration(resource_quantity,resource))

            except Exception as e:
                return {
                    'msg': 'Configuracion incorrecta de recursos'
                }


        new_configuration = Configuration(id_, name, description, resources_configurations_objects)

        Orm.create('configurations', new_configuration)
        Orm.save()

        return {
            'msg': 'Configuracion creada exitosamente',
            'configuration': asdict(new_configuration)
        }

    except Exception as e:
        return {
            'msg': str(e)
        }


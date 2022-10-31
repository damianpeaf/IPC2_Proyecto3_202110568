
from typing import Dict
from dataclasses import asdict

from ..models import Client
from ..db import Orm
from ..utils import get_value

class ResourceNotFound(Exception):
    pass

def create_client(fields:Dict):
    try:
        nit = get_value(fields, 'nit', str)
        name = get_value(fields, 'name', str)
        username = get_value(fields, 'username', str)
        password = get_value(fields, 'password', str)
        direction = get_value(fields, 'direction', str)
        email = get_value(fields, 'email', str)

        new_client = Client(nit, name, username, password, direction, email, [])
        Orm.create('clients', new_client)
        Orm.save()

        return {
            'msg': 'Cliente creado exitosamente',
            'client': asdict(new_client)
        }

    except Exception as e:
        return {
            'msg': str(e)
        }


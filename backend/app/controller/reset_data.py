from ..db import Orm

def reset_data():
    Orm.reset()
    Orm.save()

    return {
        'msg': 'Información reseteada'
    }
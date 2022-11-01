
from dataclasses import asdict
from typing import Dict
from ..db import Orm
from ..utils import get_value, eval_date_string
from datetime import datetime

class NotFoundError(Exception):
    pass

def cancel_instance(fields:Dict):
     try:
        id_ = get_value(fields, 'id', str)

        final_date = datetime.now().strftime("%d/%m/%Y")
        try:
            final_date = eval_date_string(fields['end_date'])
            if final_date == None:
                final_date = datetime.now().strftime("%d/%m/%Y")
        except:
            pass
        
        instance = Orm.searchById('instances', id_)

        if instance == None:
            raise NotFoundError(f'Instancia con la id {id_} no encontrada')

        instance.end_date = final_date
        instance.state = "Cancelada"

        return {
            "msg": "Instancia cancelada",
            "instance": asdict(instance)
        }

     except Exception as e:
        return {
            'msg': str(e)
        }

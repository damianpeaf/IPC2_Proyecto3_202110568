from dataclasses import asdict
from datetime import datetime
import uuid

from ..utils import get_value, parse_to_datetime
from ..db import Orm
from ..models import Bill, BillDetail
def generate_bill(fields):
    try:
        from_ = parse_to_datetime(get_value(fields, 'from', str))
        to_ = parse_to_datetime(get_value(fields, 'to', str))
        nit = get_value(fields, 'nit', str)

        if from_ == None or to_ == None:
            raise DateError('Formato de fecha incorrecto')

        if from_ > to_:
            raise DateError('La fecha de finalizacion tiene que ser mayor a la de inicio')


        client = Orm.searchById('clients',nit)

        if client == None:
            raise DateError(f'Cliente con nit {nit} no encontrado')
        

        details = []
        for instance in client.instances:
            for consumption in instance.consumptions:
                date = parse_to_datetime(consumption.date)
                if date < from_ or date > to_ :
                    continue

                if consumption.is_canceled:
                    continue

                instance = Orm.searchById('instances', consumption.instance_id)

                for resource_detail in instance.configuration.resources:
                    details.append(BillDetail(resource_detail.resource.id_,instance.id_, resource_detail.quantity, consumption.time))

                consumption.is_canceled = True

        bill = Bill(str(uuid.uuid1()), nit, datetime.now().strftime("%d/%m/%Y"),details)
        Orm.create('bills', bill)
        
        Orm.save()

        return {
            "bill": asdict(bill)
        }

    except Exception as e:
        return {
            "msg": str(e)
        }

class DateError(Exception):
    pass

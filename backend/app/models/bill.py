
from dataclasses import dataclass
from typing import Dict, List

from ..models import Resource, Instance

@dataclass
class BillDetail():
    resource_id : str
    instance_id : str
    quantity:float
    hours : float
    date : str
@dataclass
class Bill():
    id_ : str
    nit : str
    date : str
    detail : List[BillDetail]
    total : float = 0.0
    instance_detail : List[Dict] = None

    def __post_init__(self):
        from ..db import Orm
        self.instance_detail = []
        total = 0

        for detail in self.detail:

            resource = Orm.searchById("resources",detail.resource_id)
            instance = Orm.searchById("instances",detail.instance_id) 
            create = True

            subtotal = resource.value_per_hour * detail.quantity * detail.hours
            subtotal = round(subtotal,2 )
            total += subtotal
            total = round(total, 2)

            # check if is already registered
            for i in self.instance_detail:
                if i['instance_id'] == instance.id_:
                    # registered
                    create = False
                    i["subtotal"] += subtotal
                    i["subtotal"] = round(i["subtotal"], 2)

                    c = True
                    for r in i["consumptions"]:
                        if r["resource_id"] == resource.id_:
                            c = False
                            r['subtotal'] += subtotal
                            r['subtotal'] = round(r['subtotal'], 2)

                            r['hours_used'] += detail.hours
                            r['hours_used'] = round(r['hours_used'], 2)


                    if c:
                        i["consumptions"].append({
                            "resource_name": resource.name,
                            "resource_id": resource.id_,
                            "value_per_hour": resource.value_per_hour,
                            "resource_quantity": detail.quantity,
                            "hours_used": detail.hours,
                            "subtotal": subtotal
                        })

            # new instance
            if create:
                self.instance_detail.append({
                    "instance_id": instance.id_,
                    "instance_name": instance.name,
                    "consumptions": [{
                        "resource_name": resource.name,
                        "resource_id": resource.id_,
                        "value_per_hour": resource.value_per_hour,
                        "resource_quantity": detail.quantity,
                        "hours_used": detail.hours,
                        "subtotal": subtotal
                    }],
                    "subtotal": subtotal
                })
            

        self.total = round(total, 2)

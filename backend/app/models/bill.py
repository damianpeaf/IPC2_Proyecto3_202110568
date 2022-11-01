
from dataclasses import dataclass
import resource
from typing import List



@dataclass
class BillDetail():
    resource_id : str
    instance_id : str
    quantity:float
    hours : float

@dataclass
class Bill():
    id_ : str
    nit : str
    date : str
    detail : List[BillDetail]
    total : float = 0.0

    def __post_init__(self):
        from ..db import Orm
        total = 0
        for detail in self.detail:

            resource = Orm.searchById("resources",detail.resource_id)
            total += resource.value_per_hour * detail.quantity * detail.hours
            total = round(total, 2)

        self.total = round(total, 2)

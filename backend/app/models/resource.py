
from dataclasses import dataclass


@dataclass
class Resource():
    id_ : str
    name : str
    abreviation : str
    metric : str
    type: str
    value_per_hour: float

@dataclass
class ResourceConfiguration():
    quantity: float
    resource: Resource

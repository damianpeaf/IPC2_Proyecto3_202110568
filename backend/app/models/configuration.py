
from dataclasses import dataclass
from typing import List
from .resource import ResourceConfiguration

@dataclass
class Configuration():
    id_:str
    name: str
    description: str
    resources: List[ResourceConfiguration]

from dataclasses import dataclass
from typing import List
from .configuration import Configuration
from .consumption import Consumption
from datetime import datetime
from enum import Enum, auto

class InstanceState(Enum):
    Vigente = auto()
    Cancelada = auto()


@dataclass
class Instance():
    id_:str
    configuration: Configuration
    name: str
    init_date: datetime
    state: InstanceState
    end_date : datetime | None
    consumptions : List[Consumption]

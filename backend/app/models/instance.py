from dataclasses import dataclass
from typing import List
from .configuration import Configuration
from .consumption import Consumption
from datetime import datetime
from enum import Enum, auto


@dataclass
class Instance():
    id_:str
    configuration: Configuration
    name: str
    init_date: str
    state: str
    end_date : str | None
    consumptions : List[Consumption]

from dataclasses import dataclass
from typing import List
from .configuration import Configuration

@dataclass
class Category():
    id_ : str
    name : str
    description : str
    work_load : str
    configurations : List[Configuration]
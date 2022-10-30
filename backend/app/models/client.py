

from dataclasses import dataclass
from typing import List
from .instance import Instance

@dataclass
class Client():
    nit:str
    name:str
    username:str
    password:str
    direction:str
    email:str
    instances:List[Instance]

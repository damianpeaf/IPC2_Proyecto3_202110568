from dataclasses import dataclass
from datetime import datetime

@dataclass
class Consumption():
    client_nit : str
    instance_id : str   
    time: float
    date: datetime
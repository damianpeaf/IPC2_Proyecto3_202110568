from dataclasses import asdict
from ..db import Orm

def fetch_all_data():
    
    data = {}

    for table_name in Orm.tables.keys():
        registers = []
        for register in Orm.tables[table_name]:
            registers.append(asdict(register))
        data[table_name] = registers

    return data


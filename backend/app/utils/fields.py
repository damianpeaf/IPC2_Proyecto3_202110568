from typing import Any, Dict

def get_value(dict:Dict[str, Any], key:str, V = None):
    try:

        value = dict[key]

        if V == None:
            return value

        if isinstance(value, V):
            return value
        else:
            raise IncorrectAttributeType()
    
    except KeyError:
        raise MissingAttributeError(f"El atributo {key} es necesario")
    except IncorrectAttributeType:
        raise IncorrectAttributeType(f"El atributo {key} tiene el tipo de dato incorrecto")
    except Exception:
        raise IncorrectAttributeType(f"Ocurrió un error")
 
        

class MissingAttributeError(Exception):
    pass
class IncorrectAttributeType(Exception):
    pass
from typing import Dict, List
import xml.dom.minidom

from ..models import Consumption
from ..db import Orm
from ..utils import eval_datetime_string



def read_consumption_file(files : Dict):
    try:
        config_file = files['consumption_file']
        domTree = xml.dom.minidom.parse(config_file)
        group = domTree.documentElement

        # * Objects to create
        consumptions_objects :List[Consumption] = []

        # consumptions
        consumptions_tags = group.getElementsByTagName("consumo")
        print(len(consumptions_tags))
        for consumption_tag in consumptions_tags:

            consumption_client_nit = consumption_tag.getAttribute('nitCliente')
            consumption_instance_id = consumption_tag.getAttribute('idInstancia')
            consumption_time = float(consumption_tag.getElementsByTagName('tiempo')[0].firstChild.nodeValue)
            consumption_date = consumption_tag.getElementsByTagName('fechaHora')[0].firstChild.nodeValue
            
            if eval_datetime_string(consumption_date) == None:
                raise FileError(f'La fecha {consumption_date} no es valida, abortando creacion de consumos')
            consumption_date = eval_datetime_string(consumption_date)

            if Orm.searchById("clients", consumption_client_nit) == None:
                raise FileError(f'No existe cliente con nit {consumption_client_nit}, abortando creacion de consumos ')

            if Orm.searchById("instances", consumption_instance_id) == None:
                raise FileError(f'No existe instancia con id {consumption_instance_id}, abortando creacion de consumos')

            consumptions_objects.append(Consumption(consumption_client_nit, consumption_instance_id, consumption_time, consumption_date))

        # add consumption to instances and individual creation

        for c in consumptions_objects:
            instance = Orm.searchById('instances', c.instance_id)
            instance.consumptions.append(c)
            Orm.create('consumptions', c)

        # Orm.save()

        return {
            'msg': f'{str(len(consumptions_objects))} consumos procesados'
        }

    except KeyError:
        return {
            'msg': 'El archivo de configuración es requerido'
        }
    except FileError as e:
        return {
            'msg': str(e)
        }
    except:
        return {
            'msg': 'El archivo de configuración tiene una estructura incorrecta'
        }



class FileError(Exception):
    pass
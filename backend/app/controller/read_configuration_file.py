from typing import Dict, List
import xml.dom.minidom

from ..models import Resource, Category, Configuration, Instance, Client, ResourceConfiguration
from ..db import Orm



def read_configuration_file(files : Dict):
    try:
        config_file = files['configuration_file']
        domTree = xml.dom.minidom.parse(config_file)
        group = domTree.documentElement

        # * Objects to create
        resources_objects :List[Resource] = []
        categories_objects :List[Category] = []
        configurations_objects :List[Configuration] = []
        instances_objects :List[Instance] = []
        clients_objects :List[Client] = []

        # resources
        resources_list_tag = group.getElementsByTagName("listaRecursos")[0]
        resources_tags = resources_list_tag.getElementsByTagName("recurso")
        for resource_tag in resources_tags:
            resource_id = resource_tag.getAttribute('id')
            resource_name = resource_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
            resource_abreviation = resource_tag.getElementsByTagName('abreviatura')[0].firstChild.nodeValue
            resource_metric = resource_tag.getElementsByTagName('metrica')[0].firstChild.nodeValue
            resource_type = resource_tag.getElementsByTagName('tipo')[0].firstChild.nodeValue
            resource_value_per_hour = float(resource_tag.getElementsByTagName('valorXhora')[0].firstChild.nodeValue)

            resource = Resource(resource_id, resource_name, resource_abreviation, resource_metric, resource_type, resource_value_per_hour)
            resources_objects.append(resource)

        # categories
        categories_list_tag = group.getElementsByTagName("listaCategorias")[0]
        categories_tags = categories_list_tag.getElementsByTagName("categoria")
        for category_tag in categories_tags:
            category_id = category_tag.getAttribute('id')
            category_name = category_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
            category_description = category_tag.getElementsByTagName('descripcion')[0].firstChild.nodeValue
            category_work_load = category_tag.getElementsByTagName('cargaTrabajo')[0].firstChild.nodeValue
            
            # inside configurations 
            category_configurations_objects = []
            configuration_tags = category_tag.getElementsByTagName("configuracion")
            for configuration_tag in configuration_tags:
                configuration_id = configuration_tag.getAttribute('id')
                configuration_name = configuration_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
                configuration_description = configuration_tag.getElementsByTagName('descripcion')[0].firstChild.nodeValue

                # resource configuration
                configuration_resources_configuration = []
                configuration_resources_tags = configuration_tag.getElementsByTagName("recurso")
                for configuration_resources_tag in configuration_resources_tags:
                    # hard search resources 
                    resource_id = configuration_resources_tag.getAttribute('id')
                    resource = hard_search('resources', resource_id, resources_objects)
                    if resource == None:
                        raise FileError(f'No se encontró recurso con la id {resource_id} para la configuracion con id {configuration_id}, abortando creación')
                    resource_quantity = float(configuration_resources_tag.firstChild.nodeValue)
                    configuration_resources_configuration.append(ResourceConfiguration( resource_quantity,resource))

                configuration = Configuration(configuration_id, configuration_name, configuration_description,configuration_resources_configuration)
                configurations_objects.append(configuration)
                category_configurations_objects.append(configuration)

            # creates category
            category = Category(category_id, category_name, category_description, category_work_load, category_configurations_objects)
            categories_objects.append(category)

        # clients
        clients_list_tag = group.getElementsByTagName("listaClientes")[0]
        clients_tags = clients_list_tag.getElementsByTagName("cliente")
                
        for client_tag in clients_tags:

            client_nit = client_tag.getAttribute('nit')
            client_name = client_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
            client_username = client_tag.getElementsByTagName('usuario')[0].firstChild.nodeValue
            client_password = client_tag.getElementsByTagName('clave')[0].firstChild.nodeValue
            client_direction = client_tag.getElementsByTagName('direccion')[0].firstChild.nodeValue
            client_email = client_tag.getElementsByTagName('correoElectronico')[0].firstChild.nodeValue

            client_instances = []
            client_instances_tags = client_tag.getElementsByTagName("instancia")
            for client_instances_tag in client_instances_tags:

                instance_id = client_instances_tag.getAttribute('id')
                instance_name = client_instances_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
                instance_state = client_instances_tag.getElementsByTagName('estado')[0].firstChild.nodeValue
                instance_start_date = client_instances_tag.getElementsByTagName('fechaInicio')[0].firstChild.nodeValue
                
                instance_end_date = client_instances_tag.getElementsByTagName('fechaFinal')[0].firstChild.nodeValue if client_instances_tag.getElementsByTagName('fechaFinal')[0].firstChild else "-"
                instance_end_date = instance_end_date if instance_end_date != '-' else  None
                
                # search configuration
                instance_configuration_id = client_instances_tag.getElementsByTagName('idConfiguracion')[0].firstChild.nodeValue
                instance_configuration = hard_search("configurations", instance_configuration_id, configurations_objects)

                if instance_configuration == None:
                    raise FileError(f'No se encontró la configuracion con la id {instance_configuration_id} para la instancia con id {instance_id}, abortando creación')
                instance_consupmtions = Orm.searchById("consumptions", instance_id)
                instance = Instance(instance_id, instance_configuration, instance_name, instance_start_date, instance_state, instance_end_date,instance_consupmtions)
                instances_objects.append(instance)
                client_instances.append(instance)
            clients_objects.append(Client(client_nit, client_name, client_username, client_password, client_direction, client_email, client_instances))

        
        # creation
        warnings = []
        msgs = []

        count = 0
        for r in resources_objects:
            try:
                Orm.create('resources', r, True)
            except Exception as e:
                warnings.append(str(e))
            count += 1
        msgs.append(f'{str(count)} recursos creados')

        count = 0
        for r in categories_objects:
            try:
                Orm.create('categories', r, True)
            except Exception as e:
                warnings.append(str(e))
            count += 1
        msgs.append(f'{str(count)} categorias creadas')

        count = 0
        for r in configurations_objects:
            try:
                Orm.create('configurations', r, True)
            except Exception as e:
                warnings.append(str(e))
            count += 1
        msgs.append(f'{str(count)} configuraciones creadas')

        count = 0
        for r in instances_objects:
            try:
                Orm.create('instances', r, True)
            except Exception as e:
                warnings.append(str(e))
            count += 1
        msgs.append(f'{str(count)} instancias creadas')

        count = 0
        for r in clients_objects:
            try:
                Orm.create('clients', r, True)
            except Exception as e:
                warnings.append(str(e))
            count += 1
        msgs.append(f'{str(count)} cliente creados')

        Orm.save()

        return {
            'msgs': msgs,
            'warnings': warnings
        }

    except KeyError:
        return {
            'msg': 'El archivo de configuración es requerido'
        }
    except IndexError:
        return {
            'msg': 'El archivo de configuración tiene una estructura incorrecta'
        }
    except FileError as e:
        return {
            'msg': str(e)
        }


def hard_search(table_name : str, id_: str, not_created_list :List):

    # look in the registed
    resp = Orm.searchById(table_name, id_)

    if resp != None:
        return resp

    for item in not_created_list:
        if item.id_ == id_:
            return item
    return None


class FileError(Exception):
    pass
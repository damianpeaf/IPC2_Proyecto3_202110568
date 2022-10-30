from enum import Enum, auto
import os
from pydoc import cli
from ..models import Resource, Instance, Category, Client, Configuration, Consumption, ResourceConfiguration
from .error import InvalidObject, FileNotFound
import xml.dom.minidom


ModelType =  Resource | Instance | Category | Client | Configuration | Consumption


class Orm ():

    tables = {
        "resources" : [],
        "configurations" : [],
        "categories" : [],
        "consumptions" : [],
        "instances" : [],
        "clients" : []
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def init(cls):

        # * Reset tables

        cls.tables = {
            "resources" : [],
            "configurations" : [],
            "categories" : [],
            "consumptions" : [],
            "instances" : [],
            "clients" : [],
        }
        

        # read from db file
        project_path = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(project_path, 'backend', 'app', 'db','db.xml')

        print(db_path)

        domTree = xml.dom.minidom.parse(db_path)
        group = domTree.documentElement

        # * Fill resource tables

        resources_tags = group.getElementsByTagName("recurso")
        for resource_tag in resources_tags:

            resource_id = resource_tag.getAttribute('id')
            resource_name = resource_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
            resource_abreviation = resource_tag.getElementsByTagName('abreviatura')[0].firstChild.nodeValue
            resource_metric = resource_tag.getElementsByTagName('metrica')[0].firstChild.nodeValue
            resource_type = resource_tag.getElementsByTagName('tipo')[0].firstChild.nodeValue
            resource_value_per_hour = float(resource_tag.getElementsByTagName('valorXhora')[0].firstChild.nodeValue)

            resource = Resource(resource_id, resource_name, resource_abreviation, resource_metric, resource_type, resource_value_per_hour)
            cls.tables["resources"].append(resource)

        # * Fill configuration table

        configuration_tags = group.getElementsByTagName("configuracion")
        for configuration_tag in configuration_tags:
            configuration_id = configuration_tag.getAttribute('id')
            configuration_name = configuration_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
            configuration_description = configuration_tag.getElementsByTagName('descripcion')[0].firstChild.nodeValue

            configuration_resources_configuration = []
            configuration_resources_tags = configuration_tag.getElementsByTagName("recurso")

            for configuration_resources_tag in configuration_resources_tags:
                # search resources 
                resource_id = configuration_resources_tag.getAttribute('id')
                resource = cls.searchById(resource_id)
                resource_quantity = float(configuration_resources_tag.firstChild.nodeValue)
                configuration_resources_configuration.append(ResourceConfiguration( resource_quantity,resource))

            cls.tables["configurations"].append(Configuration(configuration_id, configuration_name, configuration_description,configuration_resources_configuration))
                

        # * Fill categories table

        categories_tags = group.getElementsByTagName("categoria")
        for category_tag in categories_tags:

            category_id = category_tag.getAttribute('id')
            category_name = category_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
            category_description = category_tag.getElementsByTagName('descripcion')[0].firstChild.nodeValue
            category_work_load = float(category_tag.getElementsByTagName('cargaTrabajo')[0].firstChild.nodeValue)
            
            
            category_configurations = []
            category_configurations_tags = category_tag.getElementsByTagName("configuracion")
            for category_configurations_tag in category_configurations_tags:
                # search configurations 
                configuration_id = category_configurations_tag.getAttribute('id')
                category_configurations.append(cls.searchById())

            cls.tables["categories"].append(Category(category_id,category_name, category_description, category_work_load, category_configurations))
                

        # * Fill consumptions table

        consumptions_tags = group.getElementsByTagName("consumo")
        for consumption_tag in consumptions_tags:

            consumption_client_nit = consumption_tag.getAttribute('nitCliente')
            consumption_instance_id = consumption_tag.getAttribute('idInstancia')
            consumption_time = float(consumption_tag.getElementsByTagName('tiempo')[0].firstChild.nodeValue)
            # ? parse to datetime
            consumption_date = consumption_tag.getElementsByTagName('fecha')[0].firstChild.nodeValue

            cls.tables["consumptions"].append(Consumption(consumption_client_nit, consumption_instance_id, consumption_time, consumption_date))


        # * Fill instances table

        instances_tags = group.getElementsByTagName("instancia")
        for instance_tag in instances_tags:
                
                instance_id = instance_tag.getAttribute('id')
                instance_name = instance_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
                
                # ? validate state
                instance_state = instance_tag.getElementsByTagName('estado')[0].firstChild.nodeValue
                
                # ? parse to datetime
                instance_start_date = instance_tag.getElementsByTagName('fechaInicio')[0].firstChild.nodeValue
                
                # ? parse to datetime
                # ? None if not exists
                instance_end_date = instance_tag.getElementsByTagName('fechaFinal')[0].firstChild.nodeValue

                # search configuration
                instance_configuration_id = instance_tag.getElementsByTagName('idConfiguracion')[0].firstChild.nodeValue
                instance_configuration = cls.searchById()

                # search consumption -> special search
                instance_consupmtions = cls.searchById()

                instance_configuration = cls.searchById()

                cls.tables["instances"].append(Instance(instance_id, instance_configuration, instance_name, instance_start_date, instance_state, instance_end_date,))

        # * Fill clients table

        clients_tags = group.getElementsByTagName("cliente")
        for client_tag in clients_tags:

            client_nit = client_tag.getAttribute('nit')
            client_name = client_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
            client_username = client_tag.getElementsByTagName('usuario')[0].firstChild.nodeValue
            client_password = client_tag.getElementsByTagName('clave')[0].firstChild.nodeValue
            client_direction = client_tag.getElementsByTagName('direccion')[0].firstChild.nodeValue
            client_email = client_tag.getElementsByTagName('correoElectronico')[0].firstChild.nodeValue

            client_instances = []
            client_instances_tags = category_tag.getElementsByTagName("instancia")
            for client_instances_tag in client_instances_tags:
                # search instances 
                instance_id = client_instances_tag.getAttribute('id')
                client_instances.append(cls.searchById())

            cls.tables["clients"].append(Client(client_nit, client_name, client_username, client_password, client_direction, client_email, client_instances))

                

    @classmethod
    def save(cls):
        pass


    # def _add_to_db_file(self, object:ModelType):


    #     domTree = None
    #     try:
    #         project_path = os.path.dirname(os.path.abspath(__file__))
    #         db_path = os.path.join(project_path, 'backend', 'app', 'db','db.xml')
    #         print(db_path)

    #         domTree = xml.dom.minidom.parse(db_path)
    #     except:
    #         domTree = None

    #         if domTree == None:
    #             raise FileNotFound
                        
    #         if isinstance(object, Resource):
    #             pass
    #         else:
    #             raise InvalidObject
        
    # def _add_text(self, file, tag, text):
    #     newScriptText = file.createTextNode( text )
    #     tag.appendChild( newScriptText  )

    # def _parse_to_object(self,table:DBTables):
    #     pass
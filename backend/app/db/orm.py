import os
from typing import Dict, List
import xml.dom.minidom

import xml.etree.ElementTree as ET
from ..models import Resource, Instance, Category, Client, Configuration, Consumption, ResourceConfiguration
from .error import IdRegisteredError


ModelType =  Resource | Instance | Category | Client | Configuration | Consumption


class Orm ():

    DB_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.xml')

    tables : Dict[str, List[ModelType]] = {
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
    def create(cls, table_name:str, object:ModelType):
        # special create for: consumptions
        if table_name == "consumptions":
            cls.tables[table_name].append(object) 
            return 

        for item in cls.tables[table_name]:
            if item.id_ == object.id_:
                raise IdRegisteredError(f'Id {object.id_} ya registrada')
                return 

        cls.tables[table_name].append(object) 

    @classmethod
    def search_all(cls, table_name:str, id_: str):
        # ? change special search here
        if table_name == "consumptions":
            return 

        registers = []
        for item in cls.tables[table_name]:
            if item.id_ == id_:
                registers.append(item)

    @classmethod
    def searchById(cls, table_name : str, id_: str):

        # special search for: consumptions
        if table_name == "consumptions":
            consumptions = []
            for item in cls.tables[table_name]:
                if item.instance_id == id_:
                    consumptions.append(item)
            return consumptions 

        for item in cls.tables[table_name]:
            if item.id_ == id_:
                return item

        print('No se encontró el objeto')
        return None

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

        domTree = xml.dom.minidom.parse(cls.DB_FILE_PATH)
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
            configuration_resources_tags = configuration_tag.getElementsByTagName("recursoConfiguracion")

            for configuration_resources_tag in configuration_resources_tags:
                # search resources 
                resource_id = configuration_resources_tag.getAttribute('id')
                resource = cls.searchById("resources", resource_id)
                if resource == None:
                    continue
                resource_quantity = float(configuration_resources_tag.firstChild.nodeValue)
                configuration_resources_configuration.append(ResourceConfiguration( resource_quantity,resource))

            cls.tables["configurations"].append(Configuration(configuration_id, configuration_name, configuration_description,configuration_resources_configuration))
                

        # * Fill categories table

        categories_tags = group.getElementsByTagName("categoria")
        for category_tag in categories_tags:

            category_id = category_tag.getAttribute('id')
            category_name = category_tag.getElementsByTagName('nombre')[0].firstChild.nodeValue
            category_description = category_tag.getElementsByTagName('descripcion')[0].firstChild.nodeValue
            category_work_load = category_tag.getElementsByTagName('cargaTrabajo')[0].firstChild.nodeValue
            
            
            category_configurations = []
            category_configurations_tags = category_tag.getElementsByTagName("configuracionCategoria")
            for category_configurations_tag in category_configurations_tags:
                # search configurations 
                configuration_id = category_configurations_tag.getAttribute('id')
                configuration = cls.searchById("configurations", configuration_id)
                if configuration == None:
                    continue
                category_configurations.append(configuration)

            cls.tables["categories"].append(Category(category_id,category_name, category_description, category_work_load, category_configurations))
                

        # * Fill consumptions table

        consumptions_tags = group.getElementsByTagName("consumo")
        for consumption_tag in consumptions_tags:

            consumption_client_nit = consumption_tag.getAttribute('nitCliente')
            consumption_instance_id = consumption_tag.getAttribute('idInstancia')
            consumption_time = float(consumption_tag.getElementsByTagName('tiempo')[0].firstChild.nodeValue)
            # ? parse to datetime
            consumption_date = consumption_tag.getElementsByTagName('fechaHora')[0].firstChild.nodeValue

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
            # instance_end_date = instance_tag.getElementsByTagName('fechaFinal')[0].firstChild.nodeValue
            instance_end_date = None

            # search configuration
            instance_configuration_id = instance_tag.getElementsByTagName('idConfiguracion')[0].firstChild.nodeValue
            instance_configuration = cls.searchById("configurations", instance_configuration_id)

            if instance_configuration == None:
                continue

            # search consumption -> special search
            instance_consupmtions = cls.searchById("consumptions", instance_id)


            cls.tables["instances"].append(Instance(instance_id, instance_configuration, instance_name, instance_start_date, instance_state, instance_end_date,instance_consupmtions))

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
            client_instances_tags = client_tag.getElementsByTagName("instanciaCliente")
            for client_instances_tag in client_instances_tags:
                # search instances 
                instance_id = client_instances_tag.getAttribute('id')
                instance = cls.searchById("instances", instance_id)
                if instance == None:
                    continue

                client_instances.append(instance)

            cls.tables["clients"].append(Client(client_nit, client_name, client_username, client_password, client_direction, client_email, client_instances))

        print('Se cargaron los datos correctamente')
                

    @classmethod
    def save(cls):
        dbRoot = ET.Element('db')

        # * Save resources table
        resources_root = ET.SubElement(dbRoot, 'listaRecursos')

        for resource in cls.tables["resources"]:
            resource_root = ET.SubElement(resources_root, 'recurso')
            resource_root.set('id', resource.id_)
            ET.SubElement(resource_root, 'nombre').text = resource.name
            ET.SubElement(resource_root, 'abreviatura').text = resource.abreviation
            ET.SubElement(resource_root, 'metrica').text = resource.metric
            ET.SubElement(resource_root, 'tipo').text = resource.type
            ET.SubElement(resource_root, 'valorXhora').text = str(resource.value_per_hour)

        # * Save configurations table
        configurationsRoot = ET.SubElement(dbRoot, 'listaConfiguraciones')

        for configuration in cls.tables["configurations"]:
            configuration_root = ET.SubElement(configurationsRoot, 'configuracion')
            configuration_root.set('id', configuration.id_)
            ET.SubElement(configuration_root, 'nombre').text = configuration.name
            ET.SubElement(configuration_root, 'descripcion').text = configuration.description
            for resource_config in configuration.resources:
                configuration_resource_root = ET.SubElement(configuration_root, 'recursoConfiguracion')
                configuration_resource_root.set('id', resource_config.resource.id_)
                configuration_resource_root.text = str(resource_config.quantity)

        # * Save categories table
        categoriesRoot = ET.SubElement(dbRoot, 'listaCategorias')

        for category in cls.tables["categories"]:
            categoryRoot = ET.SubElement(categoriesRoot, 'categoria')
            categoryRoot.set('id', category.id_)
            ET.SubElement(categoryRoot, 'nombre').text = category.name
            ET.SubElement(categoryRoot, 'descripcion').text = category.description
            ET.SubElement(categoryRoot, 'cargaTrabajo').text = category.work_load
            for configuration in category.configurations:
                configuration_root = ET.SubElement(categoryRoot, 'configuracionCategoria')
                configuration_root.set('id', configuration.id_)

        # * Save consumptions table
        consumptionsRoot = ET.SubElement(dbRoot, 'listaConsumos')

        for consumption in cls.tables["consumptions"]:
            consumptionRoot = ET.SubElement(consumptionsRoot, 'consumo')
            consumptionRoot.set('nitCliente', consumption.client_nit)
            consumptionRoot.set('idInstancia', consumption.instance_id)
            ET.SubElement(consumptionRoot, 'tiempo').text = str(consumption.time)
            # ? parse to string
            ET.SubElement(consumptionRoot, 'fechaHora').text = consumption.date

        # * Save instances table
        instancesRoot = ET.SubElement(dbRoot, 'listaInstancias')

        for instance in cls.tables["instances"]:
            instanceRoot = ET.SubElement(instancesRoot, 'instancia')
            instanceRoot.set('id', instance.id_)
            ET.SubElement(instanceRoot, 'idConfiguracion').text = instance.configuration.id_
            ET.SubElement(instanceRoot, 'nombre').text = instance.name
            ET.SubElement(instanceRoot, 'fechaInicio').text = instance.init_date
            ET.SubElement(instanceRoot, 'estado').text = instance.state
            ET.SubElement(instanceRoot, 'fechaFinal').text = instance.end_date

        # * Save clients table

        clientsRoot = ET.SubElement(dbRoot, 'listaClientes')

        for client in cls.tables["clients"]:
            clientRoot = ET.SubElement(clientsRoot, 'cliente')
            clientRoot.set('nit', client.nit)
            ET.SubElement(clientRoot, 'nombre').text = client.name
            ET.SubElement(clientRoot, 'usuario').text = client.username
            ET.SubElement(clientRoot, 'clave').text = client.password
            ET.SubElement(clientRoot, 'direccion').text = client.direction
            ET.SubElement(clientRoot, 'correoElectronico').text = client.email

            for instance in client.instances:
                instanceRoot = ET.SubElement(clientRoot, 'instanciaCliente')
                instanceRoot.set('id', instance.id_)

        # * Delete old file
        if os.path.exists(cls.DB_FILE_PATH):
            os.remove(cls.DB_FILE_PATH)

        tree = ET.ElementTree(dbRoot)
        tree.write(cls.DB_FILE_PATH,encoding='UTF-8',xml_declaration=True)
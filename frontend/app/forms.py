from django import forms

class ConfigurationMessageForm(forms.Form):
    configuration_file = forms.FileField(label="Archivo de configuracion")

class ConsumptionMessageForm(forms.Form):
    consumption_file = forms.FileField(label="Archivo de consumos")

class ResourceForm(forms.Form):
    id = forms.CharField(label="ID")
    name = forms.CharField(label="Nombre")
    abreviation = forms.CharField(label="Abreviacion")
    metric = forms.CharField(label="Metrica")
    type = forms.CharField(label="Tipo")
    value_per_hour = forms.CharField(label="Valor por hora")

class ClientForm(forms.Form):
    nit = forms.CharField(label="NIT")
    name = forms.CharField(label="Nombre")
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña")
    direction = forms.CharField(label="Direccion")
    email = forms.CharField(label="Correo electronico")


class InstanceForm(forms.Form):
    id = forms.CharField(label="ID")
    name = forms.CharField(label="Nombre") 
    configuration = forms.CharField(label="Configuracion")
    nit = forms.CharField(label="NIT")

class BillForm(forms.Form):
    nit = forms.CharField(label="NIT")
    from_ = forms.DateField(label="Fecha de inicio")
    to = forms.DateField(label="Fecha de fin")
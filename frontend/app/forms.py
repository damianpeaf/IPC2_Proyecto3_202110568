from django import forms

class ConfigurationMessageForm(forms.Form):
    configuration_file = forms.FileField(label="Archivo de configuracion")

class ConsumptionMessageForm(forms.Form):
    consumption_file = forms.FileField(label="Archivo de consumos")
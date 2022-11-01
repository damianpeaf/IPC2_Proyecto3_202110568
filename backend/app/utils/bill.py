from ..models import Configuration 

def calculate_total_price_of_configuration(conf : Configuration, hours_used : float):
    total = 0
    for detail in conf.resources:
        total +=  round(detail.quantity,2) * round(detail.resource.value_per_hour,2) * round(hours_used,2)
        total = round(total, 2)
    return round(total, 2)
from ast import match_case
import re
from datetime import datetime
def eval_datetime_string(eval_date:str):
    # regex for dd/mm/yyyy hh24:mi
    match_date = re.search('[0-9]+/[0-9]+/[0-9]+ [0-9]+:[0-9]+', eval_date.replace('-', '/'))

    if match_date is None:
        return None

    posible_date = match_date.group(0)

    try:
        date_object = datetime.strptime(posible_date, "%d/%m/%Y %H:%M")
        return date_object.strftime("%d/%m/%Y %H:%M")
    except:

        try:
            date_object = datetime.strptime(posible_date, "%Y/%m/%d %H:%M")
            return date_object.strftime("%d/%m/%Y %H:%M")
        except:
            return None


def eval_date_string(eval_date):
    # regex for dd/mm/yyyy hh24:mi
    match_date = re.search('[0-9]+/[0-9]+/[0-9]+', eval_date.replace('-', '/'))

    if match_date is None:
        return None

    posible_date = match_date.group(0)

    try:
        date_object = datetime.strptime(posible_date, "%d/%m/%Y")
        return date_object.strftime("%d/%m/%Y")
    except:
        try:
            date_object = datetime.strptime(posible_date, "%Y/%m/%d")
            return date_object.strftime("%d/%m/%Y")
        except:
            return None

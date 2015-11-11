import re


def remove_not_numbers(data=''):
    if data:
        return re.sub(r'\D', '', data)

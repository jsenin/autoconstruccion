import re


def remove_not_numbers(data=''):
    return re.sub(r'\D', '', data) if data else ''

import re


def remove_not_numbers(data=None):
    return re.sub(r'\D', '' , data)



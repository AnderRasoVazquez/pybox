# -*- coding: utf-8 -*-
"""Este modulo contiene utilidades varias."""


def format_json_key(key, value):
    """Formatea una clave y un valor en formato JSON."""
    if value.lower() not in ["true", "false"]:
        return '"%s": "%s"' % (key, value)
    else:
        return '"%s": %s' % (key, value)


def format_json(the_list):
    """Formatea una lista de claves y valores en un diccionario JSON."""
    result = "{"
    index = 0
    size = len(the_list)
    while index < size:
        result += format_json_key(the_list[index][0], the_list[index][1])
        if index != size - 1:
            result += ", "
        index += 1
    result += "}"
    return result

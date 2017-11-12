"""
Various utils
=============
"""

import json
from json.decoder import JSONDecodeError

def json_loads(data, encoding="utf-8"):
    """
    Tries ot decode a json.

    :param request: a json received from the website.
    :type request: str

    :param encoding: json encoding (e.g.: `utf-8`, `utf-16`, ...)
    :type encoding: str

    :return: dict if json is correct or None.
    """


    try:
        return json.loads(data.decode(encoding))
    except (SyntaxError, JSONDecodeError):
        pass

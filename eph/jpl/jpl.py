"""
`jpl` module contains classes and functions useful to interact with the `Jpl Horizons service`_ from NASA.

.. _`Jpl Horizons service`: https://ssd.jpl.nasa.gov/?horizons
"""


try:
    import configparser
except:
    import ConfigParser as configparser

import requests

from .models import BaseMap
from .parsers import parse
from .exceptions import *
from ..util import addparams2url, path


__all__ = ['objcode', 'codify_obj', 'codify_site', 'humanify', 'JplReq', 'JplRes']


objcode = {
    'sun': '0',
    'mercury': '199',
    'venus': '299',
    'earth': '399',
    'mars': '499',
    'jupyter': '599',
    'saturn': '699',
    'uranus': '799',
    'neptune': '899',
}


def codify_obj(name):
    """
    Translates a human readable celestial object's name to *jpl_process* code.
    
    :param str name: the name to be translated.
    :param boolean ref: whether the code has to be a reference frame code.
    :return: the *jpl_process* code.
    :rtype: str.
    """
    name = name.strip('\'@')
    return objcode.get(name, name)


def codify_site(name):
    code = codify_obj(name)
    return '\'@' + code + '\''


def humanify(code):
    """
    Translates a *jpl_process* code to a human readable celestial object's name.
    
    :param str code: the code to be translated.
    :return: the name of the celestial object.
    :rtype: str.
    """
    codeobj = dict((v, k) for k, v in objcode.items())
    return codeobj.get(code.strip("'@"), code)



class JplReq(BaseMap):
    """ Jpl Request.

    """

    JPL_ENDPOINT = 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1'

    REQUIRED_FIELDS = [
        'COMMAND',
        'START_TIME',
        'STOP_TIME',
        ]

    ALIASES = {
        'COMMAND': ['OBJECT', 'BODY'],
        'START_TIME': ['START'],
        'STOP_TIME': ['STOP'],
        'STEP_SIZE': ['STEP'],
        'CSV_FORMAT': ['CSV'],
        'TABLE_TYPE': ['TYPE'],
        'VEC_TABLE': ['TABLE'],
        }

    FILTERS = {
        'COMMAND': lambda obj: codify_obj(obj),
        'CENTER': lambda site: codify_site(site),
        'CSV_FORMAT': lambda csv: 'YES' if csv in (True, 'y', 'Y', 'yes', 'YES') else 'NO',
        }


    @staticmethod
    def aliasof(key):
        for k, aliases in JplReq.ALIASES.items():
            if key in aliases:
                return k
        return key


    @staticmethod
    def transformkey(key):
        key = key.upper()
        return JplReq.aliasof(key)


    @staticmethod
    def transformvalue(key, value):
        if key in JplReq.FILTERS:
            parser = JplReq.FILTERS[key]
            value = parser(value)
        return value


    def __getattr__(self, key):
        key = JplReq.transformkey(key)
        return super().__getattr__(key)


    def __setattr__(self, key, value):
        key = JplReq.transformkey(key)
        value = JplReq.transformvalue(key, value)
        super().__setattr__(key, value)


    def __delattr__(self, key):
        key = JplReq.transformkey(key)
        super().__delattr__(key)


    def read(self, filename, section='jplparams'):
        filename = path(filename)
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(filename)
        params = dict(config.items(section))
        return self.set(params)


    def is_valid(self):
        return all(map(lambda field: self.get(field), JplReq.REQUIRED_FIELDS))


    def url(self):
        return addparams2url(JplReq.JPL_ENDPOINT, self)


    def query(self):
        if self.is_valid():
            http_response = requests.get(JplReq.JPL_ENDPOINT, params=self)
            if http_response.status_code == 200:
                print(self.url(), http_response.status_code)
                return JplRes(http_response)
            else:
                raise ConnectionError
        else:
            raise JplBadReq



class JplRes(object):


    def __init__(self, http_response):
        self.http_response = http_response


    def get_raw(self):
        return self.http_response.text


    def get_table(self):
        return parse(self.get_raw())

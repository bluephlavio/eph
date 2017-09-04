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


__all__ = ['name2id', 'codify_obj', 'codify_site', 'humanify', 'JplReq', 'JplRes']


name2id = dict(sun=10, mercury=199, venus=299, earth=399, mars=499, jupiter=599, saturn=699, uranus=799, neptune=899)

id2name = {v: k for k, v in name2id.items()}


def codify_obj(name):
    cleaned = name.strip('\'"')
    lowered = cleaned.lower()
    if lowered in name2id.keys():
        id = name2id[lowered]
        return str(id)
    else:
        return cleaned


def codify_site(name):
    cleaned = name.strip('\'"')
    lowered = cleaned.lower()
    if lowered in name2id.keys():
        id = name2id[lowered]
        return '@' + str(id)
    elif '@' in cleaned:
        return cleaned
    else:
        return '@' + cleaned



def humanify(code):
    if code.isdigit():
        id = int(code)
    elif code.startswith('@') and code[1:].isdigit():
        id = int(code[1:])
    else:
        return code
    return id2name.get(id, code)



class JplReq(BaseMap):
    """ Jpl Request.

    """

    JPL_ENDPOINT = 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1'

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


    def url(self):
        return addparams2url(JplReq.JPL_ENDPOINT, self)


    def query(self):
        try:
            http_response = requests.get(JplReq.JPL_ENDPOINT, params=self)
        except:
            raise ConnectionError
        if http_response.status_code == 200:
            print(self.url(), http_response.status_code)
            return JplRes(http_response)
        else:
            raise JplBadReq



class JplRes(object):


    def __init__(self, http_response):
        self.http_response = http_response


    def get_raw(self):
        return self.http_response.text


    def get_table(self):
        return parse(self.get_raw())

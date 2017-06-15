"""
`jpl` module contains classes and functions useful to interact with the `Jpl Horizons service`_ from NASA.

.. _`Jpl Horizons service`: https://ssd.jpl.nasa.gov/?horizons
"""


import configparser, re
import os.path
from collections.abc import MutableMapping
from urllib.parse import urlencode

from astropy.table import Table
import requests

from eph.util import parsetable, numberify, transpose, addparams2url



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
    Translates a human readable celestial object's name to *jpl* code.
    
    :param str name: the name to be translated.
    :param boolean ref: whether the code has to be a reference frame code.
    :return: the *jpl* code.
    :rtype: str.
    """
    name = name.strip('\'@')
    return objcode.get(name, name)


def codify_site(name):
    code = codify_obj(name)
    return '\'@' + code + '\''


def humanify(code):
    """
    Translates a *jpl* code to a human readable celestial object's name.
    
    :param str code: the code to be translated.
    :return: the name of the celestial object.
    :rtype: str.
    """
    codeobj = dict((v, k) for k, v in objcode.items())
    return codeobj.get(code.strip("'@"), code)



class JplReq(MutableMapping):
    """
    Jpl Request.
    """


    JPL_ENDPOINT = 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1'
    REQUIRED_FIELDS = [
        'COMMAND',
        'START_TIME',
        'STOP_TIME',
        ]
    ALIASES = {
        'COMMAND': ['OBJECT', 'BODY'],
        }
    PARSERS = {
        'COMMAND': lambda obj: codify_obj(obj),
        'CENTER': lambda site: codify_site(site),
        }


    @staticmethod
    def aliasof(key):
        for k, v in JplReq.ALIASES.items():
            if key in v:
                return k
        return key


    @staticmethod
    def transformkey(key):
        return JplReq.aliasof(key.upper())


    @staticmethod
    def transformvalue(key, value):
        if key in JplReq.PARSERS.keys():
            parser = JplReq.PARSERS[key]
            value = parser(value)
        return value


    def __init__(self, *args, **kwargs):
        pass #self.__dict__ = dict(*args, **kwargs)


    def __getattr__(self, key):
        key = JplReq.transformkey(key)
        return self.__dict__[key]


    def __setattr__(self, key, value):
        key = JplReq.transformkey(key)
        value = JplReq.transformvalue(key, value)
        self.__dict__[key] = value


    def __getitem__(self, key):
        return self.__getattr__(key)


    def __setitem__(self, key, value):
        self.__setattr__(key, value)


    def __delitem__(self, key):
        del self.__dict__[key]


    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v


    def __len__(self):
        return len(self.__dict__)


    def read(self, filename, section='jplparams'):
        filename = os.path.abspath(os.path.expanduser(filename))
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(filename)
        params = dict(config.items(section))
        return self.set(params)


    def is_valid(self):
        return all(map(lambda x: True if self.get(x) else False, JplReq.REQUIRED_FIELDS))


    def url(self):
        return addparams2url(JplReq.JPL_ENDPOINT, self)


    def query(self):
        if self.is_valid():
            res = requests.get(JplReq.JPL_ENDPOINT, params=self)
            return JplRes(res)
        else:
            raise JplBadReq



class JplRes(object):


    def __init__(self, http_response):
        self.http_response = http_response
        self.parser = JplParser()


    def get_raw(self):
        return self.http_response.text


    def get_table(self):
        try:
            return self.parser.parse(self.http_response.text)
        except JplParserError:
            raise JplBadReq



class JplParser(object):


    EPH_REGEX = r'(?<=\$\$SOE\s)[\s\S]*?(?=\s\$\$EOE)'
    COL_NAMES_REGEX = r'(?<=\*[\r\n])[^\r\n]*(?=[\r\n]\*+\s\$\$SOE)'


    def __init__(self):
        pass


    def parse(self, source):
        data = self.data(source)
        #cols = self.cols(source)
        return Table(data)


    def data(self, source):
        match = re.search(JplParser.EPH_REGEX, source)
        if match:
            return transpose(numberify(parsetable(match.group(), delimiter=',')))
        else:
            raise JplParserError


    def cols(self, source):
        match = re.search(JplParser.COL_NAMES_REGEX, source)
        if match:
            return tuple(parsetable(match.group(), delimiter=','))
        else:
            raise JplParserError



class JplError(Exception):
    pass



class JplBadReq(JplError):
    pass



class JplParserError(JplError):
    pass






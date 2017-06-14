"""
`jpl` module contains classes and functions useful to interact with the `Jpl Horizons service`_ from NASA.

.. _`Jpl Horizons service`: https://ssd.jpl.nasa.gov/?horizons
"""


import configparser, re
import os.path
from collections import UserDict
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


def codify(name, ref=False):
    """
    Translates a human readable celestial object's name to *jpl* code.
    
    :param str name: the name to be translated.
    :param boolean ref: whether the code has to be a reference frame code.
    :return: the *jpl* code.
    :rtype: str.
    """
    name = name.strip('\'@')
    code = objcode.get(name, name)
    if ref:
        code = '\'@' + code + '\''
    return code


def humanify(code):
    """
    Translates a *jpl* code to a human readable celestial object's name.
    
    :param str code: the code to be translated.
    :return: the name of the celestial object.
    :rtype: str.
    """
    codeobj = dict((v, k) for k, v in objcode.items())
    return codeobj[code.strip("'@")]



class JplReq(UserDict):
    """
    Jpl Request.
    """


    JPL_ENDPOINT = 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1'
    REQUIRED_FIELDS = [
        'COMMAND',
        'START_TIME',
        'STOP_TIME',
        ]


    def __setitem__(self, key, value):
        if key == 'OBJECT':
            key = 'COMMAND'
            value = codify(value)
        if key == 'CENTER':
            value = codify(value, ref=True)
        super().__setitem__(key, value)


    def __getitem__(self, key):
        if key == 'OBJECT':
            key = 'COMMAND'
        return super().__getitem__(key)


    def set(self, params):
        self.update(params)
        return self


    def set_required(self, obj, start, stop):
        return self.set({
            'COMMAND': obj,
            'START_TIME': start,
            'STOP_TIME': stop,
            })


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






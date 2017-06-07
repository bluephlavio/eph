"""
`jpl` module contains classes and functions useful to interact with the `Jpl Horizons service`_ from NASA.

.. _`Jpl Horizons service`: https://ssd.jpl.nasa.gov/?horizons
"""


import configparser, requests, re, sys
from urllib.parse import urlencode
import eph
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



class JplReq(dict):
    """
    Jpl Request.
    """


    JPL_ENDPOINT = 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1'


    def __init__(self):
        dict.__init__(self)


    def set(self, params):
        self.update(params)
        return self


    def read(self, filename, section='jplparams'):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(filename)
        params = dict(config.items(section))
        self.update(params)
        return self


    def url(self):
        return addparams2url(JplReq.JPL_ENDPOINT, self)


    def query(self):
        res = requests.get(JplReq.JPL_ENDPOINT, params=self)
        return JplRes(res)


class JplRes(object):


    def __init__(self, res):
        self.res = res
        self.parser = JplParser()


    def parse(self):
        try:
            return self.parser.parse(self.res.text)
        except JplParserError:
            raise JplBadReq



class JplParser(object):


    EPH_REGEX = r'(?<=\$\$SOE\s)[\s\S]*?(?=\s\$\$EOE)'
    COL_REGEX = r'(?<=\*\s)[^\*]*?(?=\s\*+\s\$\$SOE)'


    def __init__(self):
        pass


    def parse(self, source):
        data = self.data(source)
        cols = self.cols(source)
        return eph.Eph(data, names=cols)


    def data(self, source):
        match = re.search(JplParser.EPH_REGEX, source)
        if match:
            return transpose(numberify(parsetable(match.group(), delimiter=',')))
        else:
            raise JplParserError


    def cols(self, source):
        match = re.search(JplParser.COL_REGEX, source)
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






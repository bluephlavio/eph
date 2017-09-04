""" :mod:`jpl` module

:mod:`jpl` module contains classes and functions useful to interact with the `Jpl Horizons service`_ from NASA.

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
from ..config import read_config
from ..util import addparams2url, path


__all__ = ['name2id', 'codify_obj', 'codify_site', 'humanify', 'JplReq', 'JplRes']


name2id = dict(sun=10, mercury=199, venus=299, earth=399, mars=499, jupiter=599, saturn=699, uranus=799, neptune=899)

id2name = {v: k for k, v in name2id.items()}


def codify_obj(name):
    """Tries to translate a human readable celestial object name to the corresponding Jpl Horizons code.

    If the name is not known the name itself will be returned.

    Args:
         name (str): the name to be translated.

    Returns:
        str: the code of the object (stringified version of the id).

    """
    cleaned = name.strip('\'"')
    lowered = cleaned.lower()
    if lowered in name2id.keys():
        id = name2id[lowered]
        return str(id)
    else:
        return cleaned


def codify_site(name):
    """Tries to translate a human readable celestial object name to the corresponding Jpl Horizons site code.
    If the name is not known the name itself will be returned preceded by a @ sign
    if @ is not already present in the name.

    Args:
         name (str): the name to be translated.

    Returns:
        str: the code of the site.

    """
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
    """Tries to interpret a Jpl object or site code as a human readable celestial object name.

    Args:
        code (str): the code to be translated.

    Returns:
        str: the corresponding human readable name.

    """
    if code.isdigit():
        id = int(code)
    elif code.startswith('@') and code[1:].isdigit():
        id = int(code[1:])
    else:
        return code
    return id2name.get(id, code)



class JplReq(BaseMap):
    """A requests to Jpl Horizons service.

    It can be thought as a :class:`dict` where key-value pairs represents Jpl Horizons parameters.
    Jpl parameters can be also set as attributes of the :class:`JplReq` instance.
    Furthermore, keys and values are adjusted to match Jpl Horizons interface in order to enhance
    readability and usability.

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
        """Reads configurations parameters from an ini file.

        Reads the :param:`section` section of the ini config file :param:`filename` and set all parameters
        for the Jpl request.

        Args:
            filename (str): the config file to be read.
            section (str): the section of the ini config file to be read.

        Returns:
            :class:`JplReq`: the object itself.

        """
        cp = read_config(filename)
        params = dict(cp.items(section))
        return self.set(params)


    def url(self):
        """Calculate the Jpl Horizons url corresponding to the :class:`JplReq` object.

        Returns:
            str: the url with the Jpl parameters encoded in the query string.

        """
        return addparams2url(JplReq.JPL_ENDPOINT, self)


    def query(self):
        """Performs the query to the Jpl Horizons service.

        Returns:
            :class:`JplRes`: the response from Jpl Horizons service.

        Raises:
            :class:`JplBadReq`

        """
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
    """A response from the Jpl Horizons service.
    """


    def __init__(self, http_response):
        """Initialize a :class:`JplRes` object from a `requests`_ http response object.

        Args:
            http_response: the http response from Jpl Horizons service.

        .. _`requests`: http://docs.python-requests.org/en/master/
        """
        self.http_response = http_response


    def get_raw(self):
        """Returns the content of the Jpl Horizons http response as is.
        """
        return self.http_response.text


    def get_table(self):
        """Parse the http response from Jpl Horizons and return an `astropy.table`_ object.

        .. _`astropy.table`: http://docs.astropy.org/en/stable/table/
        """
        return parse(self.get_raw())

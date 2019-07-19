"""
Contains classes and functions useful to interact with the `Jpl Horizons
service`_ from NASA.

.. _`Jpl Horizons service`: https://ssd.jpl.nasa.gov/?horizons
"""

import requests

from astropy.table import QTable

from .util import addparams2url, wrap
from .config import read_config
from .models import BaseMap
from .horizons import JPL_ENDPOINT, transform_key, transform
from .parsers import parse, get_sections


class JplReq(BaseMap):
    """
    A requests to Jpl Horizons service.

    It can be thought as a :class:`dict` where key-value pairs
    represents Jpl Horizons parameters. Jpl parameters can be also set
    as attributes of the :class:`JplReq` instance. Furthermore, keys and
    values are adjusted to match Jpl Horizons interface in order to
    enhance readability and usability.
    """

    def __getattr__(self, key):
        key = transform_key(key)
        return super(self.__class__, self).__getattr__(key)

    def __setattr__(self, key, value):
        k, v = transform(key, value)
        super(self.__class__, self).__setattr__(k, v)

    def __delattr__(self, key):
        key = transform_key(key)
        super(self.__class__, self).__delattr__(key)

    def read(self, filename, section='DEFAULT'):
        """
        Reads configurations parameters from an ini file.

        Reads the `section` section of the ini config file `filename` and set all parameters
        for the Jpl request.

        Args:
            filename (str): the config file to be read.
            section (str): the section of the ini config file to be read.

        Returns:
            :class:`JplReq`: the object itself.
        """
        params = read_config(filename, section)
        return self.set(params)

    def url(self):
        """
        Calculate the Jpl Horizons url corresponding to the :class:`JplReq`
        object.

        Returns:
            str: the url with the Jpl parameters encoded in the query string.
        """
        return addparams2url(JPL_ENDPOINT,
                             {k: wrap(str(v)) for k, v in self.items()})

    def query(self):
        """
        Performs the query to the Jpl Horizons service.

        Returns:
            :class:`JplRes`: the response from Jpl Horizons service.

        Raises:
            :class:`ConnectionError`
        """

        try:
            http_response = requests.get(self.url())
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e.__str__())

        return JplRes(http_response)


class JplRes(object):
    """A response from the Jpl Horizons service."""

    def __init__(self, http_response):
        """
        Initialize a :class:`JplRes` object from a `requests`_ http response
        object.

        Args:
            http_response: the http response from Jpl Horizons service.

        .. _`requests`: http://docs.python-requests.org/en/master/
        """
        self.http_response = http_response

    def raw(self):
        """Returns the content of the Jpl Horizons http response as is."""
        return self.http_response.text

    def get_header(self):
        header, ephem, footer = get_sections(self.raw())
        return header

    def get_data(self):
        header, data, footer = get_sections(self.raw())
        return data

    def get_footer(self):
        header, ephemeris, footer = get_sections(self.raw())
        return footer

    def parse(self, target=QTable):
        """
        Parse the http response from Jpl Horizons and return, according to
        target.

         * an `astropy.table.Table`_ object.
         * an `astropy.table.QTable`_ object.

        .. _`astropy.table.Table`: http://docs.astropy.org/en/stable/table/
        .. _`astropy.table.QTable`: http://docs.astropy.org/en/stable/table/
        """
        return parse(self.raw(), target=target)

    def __str__(self):
        return self.raw()

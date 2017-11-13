""":mod:`jpl` package contains modules related to retrieve and parse ephemeris from the `Jpl Horizons`_ service.

The main classes defined by :mod:`jpl` package are

* :class:`JplReq`: this class represents a Jpl request to the Horizons service.
  A :class:`JplReq` object is like a :class:`dict` containing Jpl service parameters used to specify an ephemeris.
* :class:`JplRes`: this represents a Jpl response from the Horizons service.
  A :class:`JplRes` object contains the http response obtained from the Horizons service through a query
  performed by a :class:`JplReq` instance. The :class:`JplRes` object can parse the response in an
  `astropy`_ table or return the raw text response.

.. _`Jpl Horizons`: https://ssd.jpl.nasa.gov/?horizons

"""


from .interface import *
from .exceptions import *

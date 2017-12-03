"""Aims to provide useful classes, functions and tools to *retrieve*, *represent* and *manipulate* ephemerides.

:mod:`eph` modules:

* :mod:`eph.eph` module contains the definition of :class:`Eph` class,
  the base class for representing an ephemeris.
  :class:`Eph` class inherits from the `astropy`_ table class (see `astropy.table.Table`_ for documentation).
* :mod:`eph.util` module contains project wide utility functions.

:mod:`eph` subpackages:

* :mod:`eph.config` subpackage contains modules and files related to project wide configurations.
* :mod:`eph.jpl` subpackage contains utility classes needed to retrieve and parse `Jpl Horizons`_ ephemerides.

.. _`astropy`: http://www.astropy.org/
.. _`astropy.table.Table`: http://docs.astropy.org/en/stable/table/
.. _`Jpl Horizons`: https://ssd.jpl.nasa.gov/?horizons
"""

from .interface import JplReq, JplRes
from .shortcuts import *

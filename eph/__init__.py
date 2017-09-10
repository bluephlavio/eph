"""Aims to provide useful classes, functions and tools to *represent*, *retrieve* and *manipulate* ephemerides.

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


import datetime

from .eph import Eph
from .jpl import JplReq, JplRes


__project__ = 'eph'
__release__ = '0.1.0'
__version__ = '.'.join(__release__.split('.')[:2])
__description__ = 'Represent, retrieve and manipulate ephemerides.'
__keywords__ = ['jpl_process', 'horizons', 'ephemeris', 'astronomy', 'planets']
__author__ = 'Flavio Grandin'
__author_email__ = 'flavio.grandin@gmail.com'
__year__ = datetime.datetime.now().year
__copyright__ = ', '.join([__author__, str(__year__)])
__license__ = 'MIT'
__url__ = 'https://github.com/bluephlavio/eph'

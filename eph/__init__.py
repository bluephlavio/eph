"""
`eph` package aims to provide useful classes, functions and tools to *represent*, *retrieve* and *manipulate* ephemerides.

* `eph.eph` module contains the definition of :class:`Eph` class, the base class for representing an ephemeris. :class:`Eph` class inherits from the astropy_ :class:`Table` class (see `astropy.table`_ for documentation).

* `eph.jpl` module contains utility classes needed to retrieve and parse `Jpl Horizons`_ ephemerides.

* `eph.util` module contains project wide utility functions.

.. _astropy: http://astropy.org
.. _`astropy.table`: http://docs.astropy.org/en/stable/table/
.. _`Jpl Horizons`: https://ssd.jpl.nasa.gov/?horizons
"""


from .eph import Eph
from .jpl import JplReq, JplRes
from .jpl.shortcuts import *

import datetime

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


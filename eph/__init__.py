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



""" Contains the definition of :class:`Eph` class, the base class for representing an ephemeris.

"""

from astropy.table import QTable


class Eph(QTable):
    """Base class for representing an ephemeris object.

    An :class:`Eph` object is an `astropy`_ Table (see `astropy.table.Table`_ for documentation).

    """

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


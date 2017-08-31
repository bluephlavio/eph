"""
`eph` module define :class:`Eph` class, the base class representing an ephemeris.
"""

from astropy.table import Table


class Eph(Table):
    """
    Base class representing an ephemeris object. An :class:`Eph` object is an `astropy`_ Table (see `astropy.table`_ for documentation).
    
    .. _`astropy`: http://astropy.org
    .. _`astropy.table`: http://docs.astropy.org/en/stable/table/
    """
    pass

""" exceptions.py

Defines Jpl Horizons related exceptions.
"""

class JplError(Exception):
    """ :class:`JplError` class

    Base class for Horizons service related errors.
    """
    pass



class JplParserError(JplError):
    """ :class:`JplParserError` class

    A :class:`JplParserError` exception is raised when problems are found in parsing a response (:class:`JplRes`)
    from Horizons service.
    """
    pass



class JplBadReq(JplError):
    """ :class:`JplBadReq` class

    A :class:`JplBadReq` exceptions is raised when a request (:class:`JplReq`) to the Horizons service cannot
    be interpreted by the system.
    """
    pass

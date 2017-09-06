"""Defines Jpl Horizons related exceptions.

"""


class JplError(Exception):
    """Base class for Horizons service related errors.

    """
    pass


class JplParserError(JplError):
    """A :class:`JplParserError` exception is raised when problems are found in parsing a response (:class:`JplRes`)
    from Horizons service.

    """
    pass


class JplBadReq(JplError):
    """A :class:`JplBadReq` exceptions is raised when a request (:class:`JplReq`) to the Horizons service cannot
    be interpreted by the system.

    """
    pass


class JplBadParam(JplError):
    """A :class:`InvalidParameter` is raised when a :class:`JplReq` tries to set a parameter that do not match
    with Jpl Horizons specifications.

    """
    pass

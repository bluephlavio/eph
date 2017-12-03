"""Defines :mod:`eph` package related exceptions.

"""


class EphError(Exception):
    """Base class for :mod:`eph` package related exceptions.

    """
    pass


class ConfigError(EphError):
    """Base class for configuration related errors.

    """
    pass


class JplError(EphError):
    """Base class for JPL Horizons service related errors.

    """
    pass


class JplBadReqError(JplError):
    """A :class:`JplBadReqError` exceptions is raised when a request to the Horizons service cannot
    be interpreted by the Horizons system.

    """
    pass


class JplBadParamError(JplError):
    """A :class:`JplBadParamError` is raised when a :class:`JplReq` tries to set a parameter
    that do not match with Jpl Horizons specifications.

    """
    pass


class ParserError(EphError):
    """A :class:`ParserError` exception is raised when problems are found in parsing
    a response from the Horizons service.

    """
    pass

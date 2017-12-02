"""Defines eph package related exceptions.

"""


class EphError(Exception):
    pass


class InvalidTargetClassError(EphError):
    """An :class:`InvalidTargetClassError` is raised when has been requested to parse a Jpl Response to an unknwon class.

    """
    pass


class ConfigError(Exception):
    """Base class for configuration related exceptions.

    """
    pass


class ConfigNotFoundError(ConfigError):
    """A :class:`ConfigNotFoundError` exception is raised when trying to read configurations from
    files that don't exist.

    """

    def __init__(self, search_list):
        self.search_list = search_list
        super(self.__class__, self).__init__()

    def format_search_list(self, delimiter=', ', bullet=str()):
        return delimiter.join(bullet + file for file in self.search_list)


class JplError(Exception):
    """Base class for Horizons service related errors.

    """
    pass


class JplParserError(JplError):
    """A :class:`JplParserError` exception is raised when problems are found in parsing a response (:class:`JplRes`)
    from Horizons service.

    """
    pass


class JplBadReqError(JplError):
    """A :class:`JplBadReqError` exceptions is raised when a request (:class:`JplReq`) to the Horizons service cannot
    be interpreted by the Horizons system.

    """
    pass


class JplBadParamError(JplError):
    """A :class:`JplBadParamError` is raised when a :class:`JplReq` tries to set a parameter that do not match
    with Jpl Horizons specifications.

    """
    pass

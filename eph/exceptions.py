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

"""Defines configuration related exceptions

"""

import os

class ConfigError(Exception):
    """Base class for configuration related exceptions.

    """


class ConfigNotFoundError(ConfigError):
    """A :class:`ConfigNotFoundError` exception is raised when trying to read configurations from
    files that don't exist.

    """

    def __init__(self, config_files):
        self.config_files = config_files
        super(self.__class__, self).__init__(self.format())


    def format(self):
        msg = 'None of the following configurations files were found:'
        list = os.linesep.join(['* ' + file for file in self.config_files])
        return os.linesep.join([msg, list])

import pkg_resources
import os.path
from shutil import copy2
from six.moves import configparser

from .util import path
from .exceptions import ConfigParserError, ConfigNotFoundError


def get_config_dir():
    return path('~/')


def get_config_file():
    return os.path.join(get_config_dir(), '.ephrc')


def get_default_config_file():
    return pkg_resources.resource_filename(__name__, 'eph.cfg')


def create_config_file(out_filename=get_config_file()):
    src_filename = get_default_config_file()
    copy2(src_filename, out_filename)


def read_config(filename=None, section=None):
    parser = configparser.ConfigParser()
    parser.optionxform = str
    config_file = path(filename) if filename else get_config_file()
    if os.path.isfile(config_file):
        try:
            parser.read(config_file)
        except configparser.ParsingError:
            raise ConfigParserError('Problems encountered parsing config file.')
        return dict(parser.items(section if section else 'DEFAULT'))
    else:
        raise ConfigNotFoundError('Config file not found.')

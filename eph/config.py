import pkg_resources
import os.path
from shutil import copy2

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from .util import path


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
    parser.read(filename if filename else get_config_file())
    return dict(parser.items(section if section else 'DEFAULT'))

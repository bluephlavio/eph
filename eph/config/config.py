import pkg_resources
import os.path
from shutil import copy2

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from eph.util import path
from .exceptions import *


def get_parser():
    parser = configparser.ConfigParser()
    parser.optionxform = str
    return parser


def get_config_dirs():
    return list(map(lambda dir: path(dir), ['~/', './']))


def get_config_files(config_file=None):
    return [path(config_file)] if config_file else list(map(lambda dir: os.path.join(dir, '.ephrc'), get_config_dirs()))


def get_default_config_file():
    return pkg_resources.resource_filename(__name__, 'config.ini')


def create_config_file(out_filename):
    src_filename = get_default_config_file()
    copy2(src_filename, out_filename)


def read_config(config_file=None):
    parser = get_parser()
    config_files = get_config_files(config_file=config_file)
    read_files = parser.read(config_files)
    if not read_files:
        raise ConfigNotFoundError(config_files)
    return parser

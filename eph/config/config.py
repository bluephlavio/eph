import pkg_resources
import os.path
from shutil import copy2

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from eph.util import path


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
    cp = configparser.ConfigParser()
    cp.optionxform = str
    config_files = cp.read(get_config_files(config_file))
    if not config_files:
        cp.read(get_default_config_file())
    return cp

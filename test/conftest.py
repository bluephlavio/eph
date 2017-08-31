import pytest

import os.path


@pytest.fixture(scope='session')
def res_dir():
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'res' + os.path.sep)


@pytest.fixture(scope='session')
def config_file(res_dir):
    return os.path.join(res_dir, 'config.ini')

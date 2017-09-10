"""Contains configuration-related data and modules.

:mod:`config` package contains:

* `config.ini`: configuration files containing all project wide default configuration.
  The file is copied at installation time to `~/.ephrc` so that it can be edited by the end user.
  If the installed file is deleted or not found by eph scripts `config.ini` configurations are kept.
* :mod:`config` module: this python module defines functions related to the creation, editing and
  storing of configurations.

"""

from .config import *
from .exceptions import *

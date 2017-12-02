"""Defines shortcut functions useful to ease the access of Jpl Horizons data.

"""

from eph.interface import *


def raw_data_from_req_file(req_file):
    """It returns a raw Jpl Horizons response from a request built from a config ini file.

    Args:
        req_file (str): the filename from which the request has to be load.

    Returns:
        str: the raw text output from Jpl.
    """

    req = JplReq().read(req_file)
    res = req.query()
    return res.raw()

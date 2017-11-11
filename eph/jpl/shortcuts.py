"""Defines shortcut functions useful to ease the access of Jpl Horizons data.

"""

from .jpl import *

def raw_data_from_req_file(req_file):
    req = JplReq().read(req_file)
    res = req.query()
    return res.raw()


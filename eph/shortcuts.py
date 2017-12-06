"""Defines shortcut functions useful to ease the access of Jpl Horizons data.

"""

from .interface import JplReq


def get(start, stop, obj, **kwargs):
    req = JplReq(
        START_TIME=start,
        STOP_TIME=stop,
        COMMAND=obj,
        **kwargs,
    )
    req.obj_data = False
    req.csv_format = True
    res = req.query()
    return res.parse()


def vec(start, stop, obj, **kwargs):
    kwargs['VEC_LABELS'] = 'NO'
    kwargs['TABLE_TYPE'] = 'VECTORS'
    kwargs['VEC_TABLE'] = '3'
    return get(start, stop, obj, **kwargs)


def pos(start, stop, obj, **kwargs):
    kwargs['VEC_LABELS'] = 'NO'
    kwargs['TABLE_TYPE'] = 'VECTORS'
    kwargs['VEC_TABLE'] = '1'
    return get(start, stop, obj, **kwargs)

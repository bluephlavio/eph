"""Defines shortcut functions useful to ease the access of Jpl Horizons data.

"""

from .interface import JplReq


def get(start, stop, obj, **kwargs):
    req = JplReq(
        START_TIME=start,
        STOP_TIME=stop,
        COMMAND=obj,
        **kwargs,
        OBJ_DATA=False,
        CSV_FORMAT=True,
    )
    res = req.query()
    return res.parse()


def vec(start, stop, obj, **kwargs):
    return get(start, stop, obj, **kwargs,
               TABLE_TYPE='V',
               VEC_LABELS=False
               )


def pos(start, stop, obj, **kwargs):
    return vec(start, stop, obj, **kwargs,
               VEC_TABLE=1
               )


def vel(start, stop, obj, **kwargs):
    return vec(start, stop, obj, **kwargs,
               VEC_TABLE=5
               )

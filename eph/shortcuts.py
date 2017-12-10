"""Defines shortcut functions useful to ease the access of Jpl Horizons data.

"""

from .interface import JplReq


def get(start, stop, obj, **kwargs):
    req = JplReq(
        START_TIME=start,
        STOP_TIME=stop,
        COMMAND=obj,
        OBJ_DATA=False,
        CSV_FORMAT=True,
        **kwargs
    )
    res = req.query()
    return res.parse()


def vec(start, stop, obj, **kwargs):
    return get(start, stop, obj,
               TABLE_TYPE='V',
               VEC_LABELS=False,
               **kwargs
               )


def pos(start, stop, obj, **kwargs):
    return vec(start, stop, obj,
               VEC_TABLE=1,
               **kwargs
               )


def vel(start, stop, obj, **kwargs):
    return vec(start, stop, obj,
               VEC_TABLE=5,
               **kwargs
               )

"""Defines shortcut functions useful to ease the access of Jpl Horizons data.

"""

from .interface import JplReq


def get(start, stop, obj, **kwargs):
    """Shortcut function to directly obtain an astropy QTable from Jpl Horizons parameters without
    building a JplReq and get a JplRes out of it to be parsed.

    Args:
        start: The start time value for the ephemeris.
        stop: The stop value for the ephemeris.
        obj: The celestial object to be targeted.

    Returns:
        :class:`astropy.table.Qtable`: The data structure containing ephemeris data.

    """
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
    """Shortcut function to directly obtain an astropy QTable with vector data.

    Args:
        start: The start time value for the ephemeris.
        stop: The stop value for the ephemeris.
        obj: The celestial object to be targeted.

    Returns:
        :class:`astropy.table.Qtable`: The data structure containing ephemeris data.

    """
    return get(start, stop, obj,
               TABLE_TYPE='V',
               VEC_LABELS=False,
               **kwargs
               )


def pos(start, stop, obj, **kwargs):
    """Shortcut function to directly obtain an astropy QTable with position-only vector data.

    Args:
        start: The start time value for the ephemeris.
        stop: The stop value for the ephemeris.
        obj: The celestial object to be targeted.

    Returns:
        :class:`astropy.table.Qtable`: The data structure containing ephemeris data.

    """
    return vec(start, stop, obj,
               VEC_TABLE=1,
               **kwargs
               )


def vel(start, stop, obj, **kwargs):
    """Shortcut function to directly obtain an astropy QTable with velocity-only vector data.

    Args:
        start: The start time value for the ephemeris.
        stop: The stop value for the ephemeris.
        obj: The celestial object to be targeted.

    Returns:
        :class:`astropy.table.Qtable`: The data structure containing ephemeris data.

    """
    return vec(start, stop, obj,
               VEC_TABLE=5,
               **kwargs
               )

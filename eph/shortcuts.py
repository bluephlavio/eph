"""Defines shortcut functions useful to ease the access of Jpl Horizons
data."""
from datetime import datetime, timedelta

from astropy.table import join

from .util import is_vector
from .interface import JplReq
from .horizons import format_time


def get(objs, dates=datetime.now(), **kwargs):
    """
    Shortcut function to directly obtain an astropy QTable from Jpl Horizons
    parameters without building a JplReq and get a JplRes out of it to be
    parsed.

    Args:
      objs: The celestial objects to be targeted.
      dates: start and stop (optional) time.

    Returns:
      :class:`astropy.table.Qtable`: The data structure containing ephemeris data.
    """
    if is_vector(dates) and len(dates) > 1:
        start, stop = format_time(dates[0]), format_time(dates[1])
    else:
        start = format_time(dates[0] if is_vector(dates) else dates)
        try:
            start_date = datetime.strptime(str(start), '%Y-%m-%d')
        except:
            start_date = datetime.strptime(str(start), '%Y-%m-%d %H:%M')
        stop_date = start_date + timedelta(1, 0, 0)
        stop = stop_date.strftime('%Y-%m-%d')
    kwargs.update({'OBJ_DATA': False, 'CSV_FORMAT': True})
    req = JplReq(START_TIME=start, STOP_TIME=stop, **kwargs)
    data = None
    keys = ['JDTDB', 'Calendar Date (TDB)']
    if not is_vector(objs):
        objs = [objs]
    for obj in objs:
        req.command = obj
        res = req.query()
        table = res.parse()
        if len(objs) > 1:
            for k, v in table.meta.items():
                table.meta[k] = [
                    v,
                ]
            for col in table.colnames:
                if col not in [
                        'Date__(UT)__HR:MN', 'JDTDB', 'Calendar Date (TDB)'
                ]:
                    table.rename_column(col, obj + '_' + col)
        if data:
            try:
                data = join(data, table, keys=keys)
            except:
                keys = [
                    'Date__(UT)__HR:MN',
                ]
                data = join(data, table, keys=keys)
        else:
            data = table
    if not is_vector(dates) or len(dates) < 2:
        data = data[:1]
    for k, v in data.meta.items():
        if all(item == v[0] for item in v):
            data.meta[k] = v[0]
    return data


def vec(objs, dates=datetime.now(), center='@0', **kwargs):
    """
    Shortcut function to directly obtain an astropy QTable with vector data.

    Args:
      objs: The celestial objects to be targeted.
      dates: start and stop (optional) time.

    Returns:
      :class:`astropy.table.Qtable`: The data structure containing ephemeris data.
    """
    kwargs.update({
        'CENTER': center,
        'TABLE_TYPE': 'V',
        'VEC_LABELS': False,
    })
    return get(objs, dates=dates, **kwargs)


def pos(objs, dates=datetime.now(), **kwargs):
    """Shortcut function to directly obtain an astropy QTable with
    position- only vector data.

    Args:
      objs: The celestial objects to be targeted.
      dates: start and stop (optional) time.

    Returns:
      :class:`astropy.table.Qtable`: The data structure containing ephemeris data.
    """
    kwargs.update({
        'VEC_TABLE': 1,
    })
    return vec(objs, dates=dates, **kwargs)


def vel(objs, dates=datetime.now(), **kwargs):
    """Shortcut function to directly obtain an astropy QTable with
    velocity- only vector data.

    Args:
      objs: The celestial objects to be targeted.
      dates: start and stop (optional) time.

    Returns:
      :class:`astropy.table.Qtable`: The data structure containing ephemeris data.
    """
    kwargs.update({
        'VEC_TABLE': 5,
    })
    return vec(objs, dates=dates, **kwargs)


def elem(objs, dates=datetime.now(), **kwargs):
    """
    Shortcut function to directly obtain an astropy QTable with orbital
    elements.

    Args:
      objs: The celestial objects to be targeted.
      dates: start and stop (optional) time.

    Returns:
      :class:`astropy.table.Qtable`: The data structure containing ephemeris data.
    """
    kwargs.update({
        'CENTER': '@0',
        'TABLE_TYPE': 'E',
    })
    return get(objs, dates=dates, **kwargs)


def obs(objs, dates=datetime.now(), **kwargs):
    """
    Shortcut function to directly obtain an astropy QTable with observable
    quantities.

    Args:
      objs: The celestial objects to be targeted.
      dates: start and stop (optional) time.

    Returns:
      :class:`astropy.table.Qtable`: The data structure containing ephemeris data.
    """
    kwargs.update({
        'CENTER': 'coord',
        'COORD_TYPE': 'GEODETIC',
        'TABLE_TYPE': 'O',
    })
    return get(objs, dates=dates, **kwargs)


def radec(objs, dates=datetime.now(), **kwargs):
    """
    Shortcut function to directly obtain an astropy QTable with RA/DEC data.

    Args:
      objs: The celestial objects to be targeted.
      dates: start and stop (optional) time.

    Returns:
      :class:`astropy.table.Qtable`: The data structure containing ephemeris data.
    """
    kwargs.update({'QUANTITIES': '1'})
    return obs(objs, dates=dates, **kwargs)


def altaz(objs, site_coord='0,0,0', dates=datetime.now(), **kwargs):
    """
    Shortcut function to directly obtain an astropy QTable with ALT/AZ data.

    Args:
      objs: The celestial objects to be targeted.
      dates: start and stop (optional) time.
      site_coord: comma separated value for longitude, latidute, altitude of a site.

    Returns:
      :class:`astropy.table.Qtable`: The data structure containing ephemeris data.
    """
    kwargs.update({'QUANTITIES': '4'})
    return obs(objs, site_coord=site_coord, dates=dates, **kwargs)

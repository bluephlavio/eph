"""Defines shortcut functions useful to ease the access of Jpl Horizons data.

"""
from datetime import datetime, timedelta

from astropy.table import join

from .util import is_vector
from .interface import JplReq
from .horizons import format_time


def get(objs, dates=datetime.now(), **kwargs):
  """Shortcut function to directly obtain an astropy QTable from Jpl Horizons parameters without
  building a JplReq and get a JplRes out of it to be parsed.

  Args:
    objs: The celestial objects to be targeted.
    dates: start and stop (optional) time.

  Returns:
    :class:`astropy.table.Qtable`: The data structure containing ephemeris data.

  """
  if is_vector(dates) and len(dates) > 1:
    start, stop = (*map(lambda date: format_time(date), dates),)
  else:
    start = format_time(dates[0] if is_vector(dates) else dates)
    try:
      start_date = datetime.strptime(str(start), '%Y-%m-%d')
    except:
      start_date = datetime.strptime(str(start), '%Y-%m-%d %H:%M')
    stop_date = start_date + timedelta(1, 0, 0)
    stop = stop_date.strftime('%Y-%m-%d')
  req = JplReq(
      START_TIME=start,
      STOP_TIME=stop,
      OBJ_DATA=False,
      CSV_FORMAT=True,
      **kwargs
  )
  data = None
  keys = ['JDTDB', 'Calendar Date (TDB)']
  if not is_vector(objs):
    objs = [objs]
  for obj in objs:
    req.command = obj
    res = req.query()
    table = res.parse()
    if len(objs) > 1:
      table.meta['Target body name'] = [table.meta['Target body name'], ]
      for col in table.colnames:
        if col not in keys:
          table.rename_column(col, obj + col)
    if data:
      data = join(data, table, keys=keys)
    else:
      data = table
  if not is_vector(dates) or len(dates) < 2:
    data = data[:1]
  return data


def vec(objs, dates=datetime.now(), center='@0', **kwargs):
  """Shortcut function to directly obtain an astropy QTable with vector data.

  Args:
    objs: The celestial objects to be targeted.
    dates: start and stop (optional) time.

  Returns:
    :class:`astropy.table.Qtable`: The data structure containing ephemeris data.

  """
  return get(objs,
             dates=dates,
             center=center,
             TABLE_TYPE='V',
             VEC_LABELS=False,
             **kwargs
             )


def pos(objs, dates=datetime.now(), **kwargs):
  """Shortcut function to directly obtain an astropy QTable with position-only vector data.

  Args:
    objs: The celestial objects to be targeted.
    dates: start and stop (optional) time.

  Returns:
    :class:`astropy.table.Qtable`: The data structure containing ephemeris data.

  """
  return vec(objs,
             dates=dates,
             VEC_TABLE=1,
             **kwargs
             )


def vel(objs, dates=datetime.now(), **kwargs):
  """Shortcut function to directly obtain an astropy QTable with velocity-only vector data.

  Args:
    objs: The celestial objects to be targeted.
    dates: start and stop (optional) time.

  Returns:
    :class:`astropy.table.Qtable`: The data structure containing ephemeris data.

  """
  return vec(objs,
             dates=dates,
             VEC_TABLE=5,
             **kwargs
             )


def elem(objs, dates=datetime.now(), **kwargs):
  """Shortcut function to directly obtain an astropy QTable with orbital elements.

  Args:
    objs: The celestial objects to be targeted.
    dates: start and stop (optional) time.

  Returns:
    :class:`astropy.table.Qtable`: The data structure containing ephemeris data.

  """
  return get(objs,
             dates=dates,
             CENTER='@0',
             TABLE_TYPE='E',
             **kwargs
             )

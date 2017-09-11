"""Defines parsing functions to read Jpl Horizons ephemeris.

"""

import re
from string import whitespace as ws

from astropy.table import QTable
from astropy import units as u

from ..util import parse_table, parse_row, numberify, transpose
from .exceptions import *


def get_sections(source):
    """Split a Jpl Horizons ephemeris in header, data and footer.

    Args:
        source (str): the content of the Jpl Horizons ephemeris data output.

    Returns:
        :class:`tuple`: a tuple of strings containing header, data and footer sections respectively.

    .. note:
       Note that whitespaces and \* are stripped out from section contents.

    """
    m = re.match(r'(.*?)\$\$SOE(.*?)\$\$EOE(.*?)', source, flags=re.DOTALL)
    if m:
        to_strip = ws + '*'
        return (m.group(i).strip(to_strip) for i in range(1, 4))
    else:
        raise JplBadReq()


def get_subsections(source):
    """Split a source string in a list of sections separated by one or more \*.

    Args:
        source (str): the source string to be splitted.

    Returns:
        :class:`list`: the lists of subsections.

    """
    to_strip = ws
    return list(map(lambda ss: ss.strip(to_strip), re.split(r'\*{3,}', source)))


def parse_jplparams(source):
    raw = re.search(r'(?<=!\$\$SOF)[\s\S]*$', source).group().strip(ws)
    return {m.group(1): m.group(2) for m in re.finditer(r'(\S*)\s=\s(\S*)', raw)}


def check_csv(source):
    jplparams = parse_jplparams(source)
    return jplparams.get('CSV_FORMAT', 'NO') == 'YES'


def parse_meta(header):
    return {m.group(1).strip(ws): m.group(2).strip(ws) for m in re.finditer(r'(.*?\D):\s(.*)', header)}


def get_units(meta):
    space_u, time_u = map(lambda unit: u.Unit(unit), meta['Output units'].lower().split('-'))
    vel_u = space_u / time_u
    return space_u, time_u, vel_u


def parse_data(data, **kwargs):
    """Parses the data section of a Jpl Horizons ephemeris in a *list of lists* table.

    Args:
        data (str): the section containing data of a Jpl Horizons ephemeris.

    Returns:
        :class:`list`: the list of lists representing a data table.

    """
    try:
        if kwargs.get('cols_del') != ',':
            raise JplParserError()
        return numberify(parse_table(data, **kwargs))
    except:
        raise JplParserError('Error parsing ephemeris...')


def parse_cols(header):
    """Finds and parses ephemeris column names in a Jpl Horizons ephemeris.

    Args:
        header (str): the header of a Jpl Horizons ephemeris.

    Returns:
        :class:`tuple`: a tuple with the names of columns.

    """
    cols_subsection = get_subsections(header)[-1]
    cols = parse_row(cols_subsection)
    return tuple(cols)


def parse(source):
    """Parses an entire Jpl Horizons ephemeris and build an `astropy`_ table out of it.

    Args:
        source (str): the content of the Jpl Horizons data file.

    Returns:
        table: the table containing data from Jpl Horizons source ephemeris.

    .. _`astropy`:  http://docs.astropy.org/en/stable/table/
    """

    cols_del = ',' if check_csv(source) else r'\s'

    header, ephem, footer = get_sections(source)
    data = transpose(parse_data(ephem, cols_del=cols_del))
    cols = parse_cols(header)
    meta = parse_meta(header)

    table = QTable(data, names=cols, meta=meta)

    space_u, time_u, vel_u = get_units(meta)
    for col in cols:
        if col.upper() in ('JDTDB',):
            table[col].unit = time_u
        elif col.upper() in ('X', 'Y', 'Z',):
            table[col].unit = space_u
        elif col.upper() in ('VX', 'VY', 'VZ',):
            table[col].unit = vel_u
        else:
            pass

    return table
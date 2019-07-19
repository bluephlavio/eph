"""Defines parsing functions to read Jpl Horizons ephemeris."""

import re
from string import whitespace as ws

from astropy import units as u
from astropy.table import Table, QTable

from .util import parse_table, parse_row, numberify, transpose, yes_or_no
from .exceptions import JplBadReqError, ParserError
from .horizons import get_col_dim


def get_sections(source):
    """
    Split a Jpl Horizons ephemeris in header, data and footer.

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
        problem_report, jplparams = map(lambda x: x.strip(ws),
                                        re.split(r'!\$\$SOF', source))
        raise JplBadReqError(problem_report)


def get_subsections(source):
    """
    Split a source string in a list of sections separated by one or more \*.

    Args:
      source (str): the source string to be splitted.

    Returns:
      :class:`list`: the lists of subsections.
    """

    to_strip = ws
    return list(map(lambda ss: ss.strip(to_strip), re.split(r'\*{3,}', source)))


def parse_params(source):
    m = re.search(r'(?<=!\$\$SOF)[\s\S]*$', source)
    if m:
        to_strip = ws
        cleaned = m.group().strip(to_strip)
        return {
            m.group(1): m.group(2)
            for m in re.finditer(r'(\S*)\s=\s(\S*)', cleaned)
        }
    return dict()


def check_csv(source):
    params = parse_params(source)
    csv = params.get('CSV_FORMAT', 'NO')
    to_strip = ws + '\'"'
    cleaned = csv.strip(to_strip)
    return yes_or_no(cleaned)


def parse_meta(header):
    meta = {
        m.group(1).strip(ws): m.group(2).strip(ws)
        for m in re.finditer(r'(.*?\D):\s(.*)', header)
    }
    meta['Target body name'] = re.match(
        r'^\S*', meta['Target body name']).group(0).lower()
    meta['Center body name'] = re.match(
        r'^\S*', meta['Center body name']).group(0).lower()
    return meta


def parse_units(meta):
    if 'Output units' in meta.keys():
        value = meta['Output units'].split(',')
        space_u, time_u = map(lambda unit: u.Unit(unit),
                              value[0].lower().split('-'))
        return dict(
            JD=u.Unit('day'),
            TIME=time_u,
            SPACE=space_u,
            VELOCITY=space_u / time_u,
            ANGLE=u.Unit('deg'),
            ANGULAR_VELOCITY=u.Unit('deg') / time_u,
        )


def parse_data(data, **kwargs):
    """
    Parses the data section of a Jpl Horizons ephemeris in a *list of lists*
    table.

    Args:
      data (str): the section containing data of a Jpl Horizons ephemeris.

    Returns:
      :class:`list`: the list of lists representing a data table.
    """

    try:
        return numberify(parse_table(data, **kwargs))
    except:
        raise ParserError


def parse_cols(header):
    """
    Finds and parses ephemeris column names in a Jpl Horizons ephemeris.

    Args:
      header (str): the header of a Jpl Horizons ephemeris.

    Returns:
      :class:`tuple`: a tuple with the names of columns.
    """

    cols_subsection = get_subsections(header)[-1]
    cols = parse_row(cols_subsection)
    return tuple(cols)


def parse(source, target=QTable):
    """
    Parses an entire Jpl Horizons ephemeris and build an `astropy`_ table out
    of it.

    Args:
      source (str): the content of the Jpl Horizons data file.
      target: the type of table to produce (Table or QTable).

    Returns:
      table: the table containing data from Jpl Horizons source ephemeris.

    .. _`astropy`:  http://docs.astropy.org/en/stable/table/
    """

    cols_del = ',' if check_csv(source) else r'\s'

    header, ephemeris, footer = get_sections(source)
    data = transpose(parse_data(ephemeris, cols_del=cols_del))
    cols = parse_cols(header)
    meta = parse_meta(header)
    units = parse_units(meta)

    if target in (Table, QTable):
        table = target(data, names=cols, meta=meta)
    else:
        raise TypeError('Available target classes are Table and QTable.')

    if units and target is not Table:
        for col in cols:
            dim = get_col_dim(col)
            if dim:
                table[col].unit = units[dim]

    return table

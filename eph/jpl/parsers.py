import re
import string

from astropy.table import Table

from ..util import parse_table, parse_row, numberify, transpose
from .exceptions import JplParserError


def get_sections(source):
    """Split a Jpl Horizons ephemeris in header, data and footer.

    Args:
        source (str): the content of the Jpl Horizons ephemeris data output.

    Returns:
        :class:`tuple`: a tuple of strings containing header, data and footer sections respectively.

    .. note:
       Note that whitespaces and * are stripped out from section contents.

    """
    m = re.match(r'(.*?)\$\$SOE(.*?)\$\$EOE(.*?)', source, flags=re.DOTALL)
    if m:
        to_strip = string.whitespace + '*'
        return (m.group(i).strip(to_strip) for i in range(1,4))
    else:
        raise JplParserError('Error trying to match structure...')


def get_subsections(source):
    """Split a source string in a list of sections separated by one or more *.

    Args:
        source (str): the source string to be splitted.

    Returns:
        :class:`list`: the lists of subsections.

    """
    to_strip = string.whitespace
    return list(map(lambda ss: ss.strip(to_strip), re.split(r'\*{1,}', source)))


def parse_data(data):
    """Parses the data section of a Jpl Horizons ephemeris in a *list of lists* table.

    Args:
        data (str): the section containing data of a Jpl Horizons ephemeris.

    Returns:
        :class:`list`: the list of lists representing a data table.

    """
    try:
        return numberify(parse_table(data))
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
    """Parses an entire Jpl Horizons ephemeris and build an `astropy.table.Table`_ out of it.

    Args:
        source (str): the content of the Jpl Horizons data file.

    Returns:
        :class:`astropy.table.Table`: the table containing data from Jpl Horizons source ephemeris.

    """
    header, ephemeris, footer = get_sections(source)
    data = transpose(parse_data(ephemeris))
    cols = parse_cols(header)
    return Table(data, names=cols)

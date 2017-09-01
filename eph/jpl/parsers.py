import re
import string

from astropy.table import Table

from ..util import parse_table, parse_row, numberify, transpose
from .exceptions import JplParserError


def get_sections(source):
    m = re.match(r'(.*?)\$\$SOE(.*?)\$\$EOE(.*?)', source, flags=re.DOTALL)
    if m:
        to_strip = string.whitespace + '*'
        return (m.group(i).strip(to_strip) for i in range(1,4))
    else:
        raise JplParserError('Error trying to match structure...')


def get_subsections(source):
    to_strip = string.whitespace
    return list(map(lambda ss: ss.strip(to_strip), re.split(r'\*{1,}', source)))


def parse_data(data):
    try:
        return numberify(parse_table(data))
    except:
        raise JplParserError('Error parsing ephemeris...')


def parse_cols(header):
    cols_subsection = get_subsections(header)[-1]
    cols = parse_row(cols_subsection)
    return tuple(cols)


def parse(source):
    header, ephemeris, footer = get_sections(source)
    data = transpose(parse_data(ephemeris))
    cols = parse_cols(header)
    return Table(data, names=cols)

import copy
from urllib.parse import urlparse, urlunparse, urlencode
from os.path import abspath, expanduser
import string


def is_vector(obj):
    return hasattr(obj, '__iter__') and not isinstance(obj, str)


def clean_row(row):
    to_strip = string.whitespace
    return list(map(lambda cell: cell.strip(to_strip), row))


def parse_row(raw, cols_del=','):
    to_strip = string.whitespace + cols_del
    row = raw.strip(to_strip).split(cols_del)
    return clean_row(row)


def parse_table(raw, cols_del=',', rows_del='\n'):
    to_strip = string.whitespace + rows_del + cols_del
    rows = raw.strip(to_strip).split(rows_del)
    return list(map(lambda row: parse_row(row, cols_del=cols_del), rows))


def numberify(data):
    numberified = copy.deepcopy(data)
    if is_vector(numberified):
        return list(map(lambda obj: numberify(obj), numberified))
    else:
        try:
            return float(numberified)
        except (TypeError, ValueError):
            return numberified


def transpose(data):
    return [list(row) for row in zip(*data)]


def path(filename):
    return abspath(expanduser(filename))


def addparams2url(url, params):
    if urlparse(url).query:
        return url + '&' + urlencode(params)
    else:
        return urlunparse(urlparse(url)) + '?' + urlencode(params)


def quote(s):
    if s.startswith('\'') and s.endswith('\''):
        return s
    if s.startswith('"') and s.endswith('"'):
        return '\'' + s[1:-1] + '\''
    return '\'' + s + '\''


def yes_or_no(value, y='YES', n='NO'):
    value = value.lower() if isinstance(value, str) else value
    if value in ('y', 'yes', 'true', True, 1):
        return y
    elif value in ('n', 'no', 'false', False, 0):
        return n
    else:
        return None

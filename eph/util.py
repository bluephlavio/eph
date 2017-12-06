import copy
import os.path
import string
import re
from six.moves.urllib.parse import urlparse, urlunparse, urlencode


def is_vector(obj):
    return hasattr(obj, '__iter__') and not isinstance(obj, str)


def clean_row(row):
    to_strip = string.whitespace
    return list(map(lambda cell: cell.strip(to_strip), row))


def parse_row(raw, cols_del=r','):
    to_strip = string.whitespace + cols_del
    cleaned = raw.strip(to_strip)
    row = re.split(cols_del, cleaned)
    return clean_row(row)


def parse_table(raw, cols_del=r',', rows_del=r'\r?\n'):
    to_strip = string.whitespace + rows_del + cols_del
    cleaned = raw.strip(to_strip)
    rows = re.split(rows_del, cleaned)
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
    return os.path.abspath(os.path.expanduser(filename))


def addparams2url(url, params):
    if urlparse(url).query:
        return url + '&' + urlencode(params)
    else:
        return urlunparse(urlparse(url)) + '?' + urlencode(params)


def wrap(s, wrapper='\'', to_strip='"'):
    cleaned = s.strip(to_strip)
    if cleaned.startswith(wrapper) and cleaned.endswith(wrapper):
        return cleaned
    return wrapper + cleaned + wrapper


def yes_or_no(value, yes='YES', no='NO'):
    value = value.lower() if isinstance(value, str) else value
    if value in ('y', 'yes', 'true', '1', True, 1):
        return yes
    elif value in ('n', 'no', 'false', '0', False, 0):
        return no

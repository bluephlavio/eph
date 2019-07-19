"""Defines variables and functions used to interfacing with JPL Horizons
system."""

from datetime import datetime
from astropy.time import Time

from .util import wrap, yes_or_no
from .exceptions import JplBadParamError

JPL_ENDPOINT = 'https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1'

JPL_PARAMS = {
    # target
    'COMMAND',
    # time
    'START_TIME',
    'STOP_TIME',
    'STEP_SIZE',
    'TLIST',
    'TIME_ZONE',
    # reference
    'REF_PLANE',
    'REF_SYSTEM',
    'CENTER',
    'COORD_TYPE',
    'SITE_COORD',
    # switches
    'MAKE_EPHEM',
    # output
    'TABLE_TYPE',
    'QUANTITIES',
    'VEC_TABLE',
    'VEC_CORR',
    'APPARENT',
    'TIME_DIGITS',
    'OUT_UNITS',
    'RANGE_UNITS',
    'SUPPRESS_RANGE_RATE',
    'ELEV_CUT',
    'SKIP_DAYLT',
    'SOLAR_ELONG',
    'AIRMASS',
    'LHA_CUTOFF',
    'EXTRA_PREC',
    'VEC_DELTA_T',
    'TP_TYPE',
    'R_T_S_ONLY',
    'CA_TABLE_TYPE',
    'TCA3SG_LIMIT',
    'CALIM_SB',
    'CALIM_PL',
    # format
    'CSV_FORMAT',
    'CAL_FORMAT',
    'ANG_FORMAT',
    'VEC_LABELS',
    'ELM_LABELS',
    'OBJ_DATA',
}

# key-value translation


def transform_key(key):
    """
    Tranforms an input key to a Jpl-compatible parameter key.

    Args:
        key (str): the key to be interpreted and translated.

    Returns:
        str: the interpreted Jpl-compatible key.

    Raises:
        :class:`JplBadParamError`
    """
    key = key.upper().replace('-', '_')
    if key in JPL_PARAMS:
        return key
    for param, aliases in ALIASES.items():
        if key in aliases:
            return param
    raise JplBadParamError(
        '\'{0}\' cannot be interpreted as a Jpl Horizons parameter'.format(key))


def transform_value(key, value):
    """
    Tries to transforms an input value into a Jpl-compatible one or it leaves
    as is.

    Args:
        key (str): the Jpl-compatible key.
        value: a ``str`` to be translated or an object such as ``str(value)``
        can be interpreted by Jpl.

    Returns:
        str: the transofrmed value.
    """
    for filter_, params in FILTERS.items():
        if key in params:
            return filter_(value)
    return value


def transform(key, value):
    """
    Transforms an input key-value pair in a Jpl-compatible one.

    Args:
        key (str): the key to be interpreted or translated.
        value: a ``str`` to be translated or the object such as ``str(value)`` is Jpl-compatible.

    Returns:
        tuple: the final key-value pair.
    """
    k = transform_key(key)
    v = transform_value(k, value)
    return k, v


def is_jpl_param(key):
    """
    Checks if a key is a Jpl Horizons parameter or a defined alias.

    Args:
        key (str): the parameter to be checked.

    Returns:
        boolean: Whether key is or not a Jpl parameter.
    """
    try:
        if transform_key(key) in JPL_PARAMS:
            return True
        else:
            return False
    except JplBadParamError:
        return False


# object-name translation

NAME2ID = dict(
    sun=10,
    mercury=199,
    venus=299,
    earth=399,
    mars=499,
    jupiter=599,
    saturn=699,
    uranus=799,
    neptune=899,
)

ID2NAME = {v: k for k, v in NAME2ID.items()}


def codify_obj(name):
    """
    Tries to translate a human readable celestial object name to the
    corresponding Jpl Horizons code. If the name is not known the name itself
    will be returned.

    Args:
         name (str): the name to be translated.

    Returns:
        str: the code of the object (stringified version of the id).
    """
    stringified = str(name)
    cleaned = stringified.strip('\'"')
    lowered = cleaned.lower()
    if lowered in NAME2ID.keys():
        id_ = NAME2ID[lowered]
        return str(id_)
    else:
        return cleaned


def codify_site(name):
    """
    Tries to translate a human readable celestial object name to the
    corresponding Jpl Horizons site code.

    If the name is not known the name itself will be returned preceded by a @ sign
    if @ is not already present in the name.

    Args:
         name (str): the name to be translated.

    Returns:
        str: the code of the site.
    """
    cleaned = name.strip('\'"')
    lowered = cleaned.lower()
    if lowered in NAME2ID.keys():
        id_ = NAME2ID[lowered]
        return '@' + str(id_)
    elif '@' in cleaned:
        return cleaned
    elif cleaned in (
            'coord',
            'geo',
    ):
        return cleaned
    else:
        return '@' + cleaned


def humanify(code):
    """
    Tries to interpret a Jpl object or site code as a human readable celestial
    object name.

    Args:
        code (str): the code to be translated.

    Returns:
        str: the corresponding human readable name.
    """
    if code.isdigit():
        id_ = int(code)
    elif code.startswith('@') and code[1:].isdigit():
        id_ = int(code[1:])
    else:
        return code
    return ID2NAME.get(id_, code)


# dimensions and units

DIM_COL = dict(
    # dimension: columns
    JD={
        'JDTDB',
        'Tp',
    },
    TIME={
        'LT',
    },
    SPACE={
        'X',
        'Y',
        'Z',
        'RG',
        'QR',
        'A',
        'AD',
    },
    VELOCITY={
        'VX',
        'VY',
        'VZ',
        'RR',
    },
    ANGLE={
        'IN',
        'OM',
        'W',
        'MA',
        'TA',
    },
    ANGULAR_VELOCITY={
        'N',
    },
)


def get_col_dim(col):
    """
    Get the physical dimension of a column by its name.

    Args:
        col (str): the name of the column.

    Returns:
        str: the physical dimensions of the given column.
    """
    for dim in DIM_COL.keys():
        if col in DIM_COL[dim]:
            return dim


def format_time(t):
    """
    Modify time data t so that str(t) can be interpreted by Jpl.

    Args:
        t: the time data. It can be a str, an astropy.time.Time object
        or an object such as str(t) can be understood by Jpl.

    Returns:
        the final object.
    """
    if type(t) == Time:
        t.out_subfmt = 'date_hm'
    elif type(t) == datetime:
        return t.strftime('%Y-%m-%d %H:%M')
    return t


# aliases and filters

ALIASES = dict(
    COMMAND={
        'OBJECT',
        'OBJ',
        'BODY',
        'TARGET',
    },
    START_TIME={
        'START',
        'BEGIN',
        'FROM',
    },
    STOP_TIME={
        'STOP',
        'END',
        'TO',
    },
    STEP_SIZE={
        'STEP',
        'STEPS',
    },
    CENTER={
        'ORIGIN',
    },
    CSV_FORMAT={
        'CSV',
    },
    TABLE_TYPE={
        'TYPE',
    },
    VEC_TABLE={
        'TABLE',
    },
)

FILTERS = {
    codify_obj: ['COMMAND',],
    codify_site: ['CENTER',],
    wrap: ['TLIST',],
    yes_or_no: [
        'CSV_FORMAT',
        'MAKE_EPHEM',
        'OBJ_DATA',
        'VEC_LABELS',
    ],
    format_time: [
        'START_TIME',
        'STOP_TIME',
    ],
}

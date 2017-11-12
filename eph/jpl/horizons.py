"""Defines variables and functions used to interfacing with Jpl Horizons system.

"""
from astropy.time import Time

from ..util import wrap, yes_or_no


JPL_ENDPOINT = 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1'


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
    'APPARTENT',
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


# object name translation

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
    """Tries to translate a human readable celestial object name to the corresponding Jpl Horizons code.

    If the name is not known the name itself will be returned.

    Args:
         name (str): the name to be translated.

    Returns:
        str: the code of the object (stringified version of the id).

    """
    cleaned = name.strip('\'"')
    lowered = cleaned.lower()
    if lowered in NAME2ID.keys():
        id = NAME2ID[lowered]
        return str(id)
    else:
        return cleaned


def codify_site(name):
    """Tries to translate a human readable celestial object name to the corresponding Jpl Horizons site code.
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
        id = NAME2ID[lowered]
        return '@' + str(id)
    elif '@' in cleaned:
        return cleaned
    else:
        return '@' + cleaned


def humanify(code):
    """Tries to interpret a Jpl object or site code as a human readable celestial object name.

    Args:
        code (str): the code to be translated.

    Returns:
        str: the corresponding human readable name.

    """
    if code.isdigit():
        id = int(code)
    elif code.startswith('@') and code[1:].isdigit():
        id = int(code[1:])
    else:
        return code
    return ID2NAME.get(id, code)


# key-value translation

def transform_key(key):
    key = key.upper().replace('-', '_')
    if key in JPL_PARAMS:
        return key
    for jplparam, aliases in ALIASES.items():
        if key in aliases:
            return jplparam


def transform_value(key, value):
    for filter, jplparams in FILTERS.items():
        if key in jplparams:
            return filter(value)
    return value


def transform(key, value):
    k = transform_key(key)
    v = transform_value(k, value)
    return k, v


# dimensions and units

DIM_COL = dict(
    # dimension: columns
    JD={'JDTDB', 'Tp',},
    TIME={'LT',},
    SPACE={'X', 'Y', 'Z', 'RG', 'QR', 'A', 'AD',},
    VELOCITY={'VX', 'VY', 'VZ', 'RR',},
    ANGLE={'IN', 'OM', 'W', 'MA', 'TA',},
    ANGULAR_VELOCITY={'N',},
)


def get_col_dim(col):
    for dim in DIM_COL.keys():
        if col in DIM_COL[dim]:
            return dim


def format_time(t):
    if type(t) == Time:
        t.out_subfmt = 'date_hm'
    return t


# aliases and filters

ALIASES = dict(
    COMMAND={'OBJECT', 'OBJ', 'BODY', 'TARGET',},
    START_TIME={'START', 'BEGIN', 'FROM',},
    STOP_TIME={'STOP', 'END', 'TO',},
    STEP_SIZE={'STEP', 'STEPS',},
    CENTER={'ORIGIN',},
    CSV_FORMAT={'CSV',},
    TABLE_TYPE={'TYPE',},
    VEC_TABLE={'TABLE',},
)


FILTERS = {
    codify_obj: ['COMMAND'],
    codify_site: ['CENTER'],
    wrap: ['TLIST'],
    yes_or_no: ['CSV_FORMAT', 'MAKE_EPHEM', 'OBJ_DATA', 'VEC_LABELS'],
    format_time: ['START_TIME', 'STOP_TIME'],
}


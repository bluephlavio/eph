import argparse
import logging
import sys
from six.moves import configparser

from astropy.table import Table

from .exceptions import *
from .horizons import codify_obj, codify_site, is_jpl_param
from .interface import JplReq


formatter = logging.Formatter('%(levelname)s: %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.addHandler(console_handler)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Retrive, parse and format Jpl Horizons ephemerides.',
    )
    parser.add_argument('start',
                        metavar='TIME_START',
                        help='''specifies ephemeris start time
                        (i.e. YYYY-MMM-DD {HH:MM} {UT/TT}) ... where braces "{}"
                        denote optional inputs'''
                        )
    parser.add_argument('stop',
                        metavar='STOP_TIME',
                        help='''specifies ephemeris stop time
                        (i.e. YYYY-MMM-DD {HH:MM} {UT/TT}) ... where braces "{}"
                        denote optional inputs''')
    parser.add_argument('object',
                        metavar='COMMAND',
                        type=codify_obj,
                        help='program to execute OR target object to select for data & ephemeris output')
    parser.add_argument('--center', '-c',
                        type=codify_site,
                        help='''
                        selects coordinate origin. Can be observing site
                        name, ID#, 'coord' (which uses values stored in
                        "SITE_COORD" and "COORD_TYPE") or 'geo' (geocentric)
                        ''')
    parser.add_argument('--coord-type',
                        choices=['GEODETIC', 'CYLINDRICAL'],
                        help='''
                        selects type of user coordinates in SITE_COORD.
                        Used only when CENTER = 'coord'.
                        Values: GEODETIC or CYLINDRICAL
                        ''')
    parser.add_argument('--site-coord',
                        help='sets coordinates of type COORD_TYPE')
    parser.add_argument('--step', '-s',
                        metavar='STEP_SIZE',
                        help='''
                        gives ephemeris output print step in form:
                        integer# {units} {mode}
                        ''')
    parser.add_argument('--cal-format',
                        choices=['CAL', 'JD', 'BOTH'],
                        help='''
                        selects type of date output when
                        TABLE_TYPE=OBSERVER. Values can be CAL, JD or BOTH
                        ''')
    parser.add_argument('--ref-plane',
                        choices=['E', 'F', 'B'],
                        help='''
                        table reference plane;
                        ECLIPTIC (E), FRAME (F) or 'BODY EQUATOR' (B)
                        ''')
    parser.add_argument('--ref-system',
                        choices=['J2000', 'B1950'],
                        help='''
                        specifies reference frame for any geometric and
                        astrometric quantities. Values: 'J2000' for ICRF/J2000.0,
                        or 'B1950' for FK4/B1950.0
                        ''')
    parser.add_argument('--make-ephem',
                        choices=['YES', 'NO'],
                        help='toggles generation of ephemeris, if possible')
    parser.add_argument('--table-type', '-t',
                        choices=['O', 'V', 'E', 'A'],
                        help='''
                        selects type of table to generate, if possible.
                        Values: OBSERVER (O), ELEMENTS (E), VECTORS (V), APPROACH (A)
                        ''')
    parser.add_argument('--vec-table',
                        choices=[str(i) for i in range(1, 7)],
                        help='''
                        selects table format when TABLE_TYPE=VECTOR.
                        Values can be a single integer from 1 to 6
                        ''')
    parser.add_argument('--time-digits',
                        choices=['MINUTES', 'SECONDS', 'FRACSECONDS'],
                        help='controls output precision')
    parser.add_argument('--time-zone',
                        help='''
                        specifies local civil time offset, relative
                        to UT, in the format {s}HH{:MM}
                        ''')
    parser.add_argument('--vec-corr',
                        choices=['NONE', 'LT', 'LT+S'],
                        help='''
                        selects level of correction to output vectors
                        when TABLE_TYPE=VECTOR. Values are NONE (geometric states),
                        'LT' (astrometric states) or
                        'LT+S' (astrometric states corrected for stellar aberration)
                        ''')
    parser.add_argument('--out-units', '-u',
                        choices=['KM-S', 'AU-D', 'KM-D'],
                        help='''
                        selects output units when TABLE_TYPE=VECTOR or ELEMENT.
                        Values can be KM-S, AU-D, KM-D indicating distance and time units
                        ''')
    parser.add_argument('--range-units',
                        choices=['AU', 'KM'],
                        help='''
                        sets the units on range quantities output when
                        TABLE_TYP=OBS (i.e. delta and r)
                        ''')
    parser.add_argument('--suppress-range-rate',
                        choices=['YES', 'NO'],
                        help='''
                        sets turns off output of delta-dot
                        and rdot (range-rate) quantities when TABLE_TYP=OBS
                        ''')
    parser.add_argument('--ang-format',
                        choices=['HMS', 'DEG'],
                        help='selects RA/DEC output when TABLE_TYPE=OBSERVER')
    parser.add_argument('--csv',
                        choices=['YES', 'NO'],
                        help='toggles output of table in comma-separated value format')
    parser.add_argument('--vec-labels', '-l',
                        choices=['YES', 'NO'],
                        help='''
                        toggles labelling of each vector component.
                        That is, symbols like "X= ###### Y= ##### Z= ######" will
                        appear in the output. If CSV_FORMAT is YES, this parameter is ignored
                        ''')
    parser.add_argument('--obj-data',
                        choices=['YES', 'NO'],
                        help='''toggles return of object summary data''')
    parser.add_argument('--apparent',
                        choices=['AIRLESS', 'REFRACTED'],
                        help='''
                        toggles refraction correction of apparent
                        coordinates if users set TABLE_TYPE=OBSERVER
                        ''')
    parser.add_argument('--config',
                        help='specifies a configuration file to be used')
    parser.add_argument('--output', '-o',
                        default=sys.stdout,
                        help='specify the output filename')
    parser.add_argument('--format',
                        default='ascii',
                        help='specify how the data table must be formatted')
    parser.add_argument('--raw',
                        action='store_true',
                        help='disables parsing of horizons output')
    parser.add_argument('--ephem-only',
                        action='store_true',
                        help='strip header and footer of a raw Jpl Horizons response')
    parser.add_argument('--suppress-warnings',
                        action='store_true',
                        help='suppress warnings such as missing config files etc..')
    return parser


def parse_args(args):
    parser = get_parser()
    return parser.parse_args(args)


def build_request(ns):

    req = JplReq()

    try:
        req.read(ns.config)
    except ConfigError:
        if ns.config:
            raise
        elif ns.suppress_warnings:
            pass
        else:
            logger.warning('Configuration file not found.')

    req.set({
        k: v for k, v in vars(ns).items() if is_jpl_param(k) and v
    })

    return req


def get_data(res, ns):
    if ns.raw:
        if ns.ephem_only:
            return res.get_data()
        return res.raw()
    else:
        return res.parse()


def write(data, ns):
    if isinstance(data, Table) and ns.format:
        data.write(ns.output, format=ns.format)
    else:
        if ns.output is sys.stdout:
            sys.stdout.write(data)
        else:
            with open(ns.output, 'w') as f:
                f.write(data)


def main():

    ns = parse_args(sys.argv[1:])

    try:
        req = build_request(ns)
    except ConfigError:
        logger.error('Configuration file not found.')
        sys.exit(-1)
    except configparser.ParsingError as e:
        logger.error('Problems encountered while parsing configuration files:\n\t' + str(e))
        sys.exit(-1)

    try:
        res = req.query()
    except ConnectionError as e:
        logger.error('Connection error:\n\t' + str(e))
        sys.exit(-1)

    try:
        data = get_data(res, ns)
    except JplBadReqError as e:
        logger.error('Horizons cannot interpret the request. Horizons says:\n\t' + e.__str__())
        sys.exit(-1)
    except ParserError:
        logger.error('''
            eph cannot parse this format.
            Try passing --csv YES option or --raw to get Horizons response as is.
        ''')
        sys.exit(-1)

    try:
        write(data, ns)
    except IOError as e:
        logger.error('''Problems trying to write data:\n\t''' + str(e))

if __name__ == '__main__':
    main()

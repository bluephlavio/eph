import argparse
import logging
import sys
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from eph.jpl.jpl import *
from eph.jpl.parsers import *


formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
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
    parser.add_argument('--ref-plane', '-p',
                        choices=['E', 'F', 'B'],
                        help='''
                        table reference plane; 
                        ECLIPTIC (E), FRAME (F) or 'BODY EQUATOR' (B)
                        ''')
    parser.add_argument('--ref-system', '-r',
                        choices=['J2000', 'B1950'],
                        help='''
                        specifies reference frame for any geometric and
                        astrometric quantities. Values: 'J2000' for ICRF/J2000.0,
                        or 'B1950' for FK4/B1950.0
                        ''')
    parser.add_argument('--make-ephem',
                        action='store_true',
                        help='toggles generation of ephemeris, if possible')
    parser.add_argument('--table-type', '-t',
                        choices=['O', 'V', 'E', 'A'],
                        help='''
                        selects type of table to generate, if possible.
                        Values: OBSERVER (O), ELEMENTS (E), VECTORS (V), APPROACH (A)
                        ''')
    parser.add_argument('--vec-table', '-v',
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
    parser.add_argument('--units', '-u',
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
                        action='store_true',
                        help='''
                        sets turns off output of delta-dot
                        and rdot (range-rate) quantities when TABLE_TYP=OBS
                        ''')
    parser.add_argument('--ang-format',
                        choices=['HMS', 'DEG'],
                        help='selects RA/DEC output when TABLE_TYPE=OBSERVER')
    parser.add_argument('--csv',
                        action='store_true',
                        help='toggles output of table in comma-separated value format')
    parser.add_argument('--vec-label', '-l',
                        action='store_true',
                        help='''
                        toggles labelling of each vector component.
                        That is, symbols like "X= ###### Y= ##### Z= ######" will
                        appear in the output. If CSV_FORMAT is YES, this parameter is ignored
                        ''')
    parser.add_argument('--obj-data',
                        action='store_true',
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
    return parser


def build_request(args):
    req = JplReq()
    req.read(args.config)
    logger.info('jplparams defaults read')
    req.set({
        k: v for k, v in vars(args).items() if transform_key(k) in JPL_PARAMS and v
    })
    logger.info('command line jplparams read')
    return req


def get_data(req, args):
    res = req.query()
    logger.info('jpl response obtained')
    if args.raw:
        raw = res.get_raw()
        if args.ephem_only:
            header, ephem, footer = get_sections(raw)
            return ephem
        return raw
    else:
        logger.info('ready to parse jpl response')
        return res.get_table()


def write(data, args):
    if isinstance(data, Table) and args.format:
        data.write(args.output, format=args.format)
    else:
        if args.output is sys.stdout:
            sys.stdout.write(data)
        else:
            with open(args.output, 'w') as f:
                f.write(data)


def process(args):
    req = build_request(args)
    data = get_data(req, args)
    write(data, args)
    logger.info('data written')


def main():
    try:
        parser = get_parser()
        args = parser.parse_args()
        process(args)
    except configparser.ParsingError as e:
        logger.error('Error trying to parse configuration file:\n' + str(e))
    except Exception as e:
        logger.error(str(e))


if __name__ == '__main__':
    main()

"""eph console script module."""

import argparse
import logging
import sys
from datetime import datetime

from astropy.table import Table

from .exceptions import *
from .horizons import codify_obj, codify_site, is_jpl_param, transform_key
from .interface import JplReq
from .shortcuts import get
from .config import read_config

# logger

formatter = logging.Formatter('%(levelname)s: %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.addHandler(console_handler)

# parser

parser = argparse.ArgumentParser(
    description='Retrive, parse and format Jpl Horizons ephemerides.',)
parser.add_argument(
    'objs',
    nargs='+',
    metavar='objects',
    help=
    'program to execute OR target object to select for data & ephemeris output')
parser.add_argument('--dates',
                    nargs='+',
                    metavar='dates',
                    default=datetime.now(),
                    help='''specifies ephemeris start and stop times
                    (i.e. YYYY-MMM-DD {HH:MM} {UT/TT}) ... where braces "{}"
                    denote optional inputs''')
parser.add_argument('--center',
                    '-c',
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
parser.add_argument('--site-coord', help='sets coordinates of type COORD_TYPE')
parser.add_argument('--step',
                    '-s',
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
parser.add_argument('--table-type',
                    '-t',
                    choices=['O', 'V', 'E', 'A'],
                    help='''
                    selects type of table to generate, if possible.
                    Values: OBSERVER (O), ELEMENTS (E), VECTORS (V), APPROACH (A)
                    ''')
parser.add_argument('--quantities',
                    '-q',
                    help='''
                    only if --table-type=O. It is a list
                    of desired output quantity codes. If multiple quantities
                    desired, separate with commas and enclose in quotes.
                    "*" denotes output affected by
                    refraction model, ">" indicates statistical values
                    derived from a covariance matrix.
                    1. Astrometric RA & DEC
                    *2. Apparent RA & DEC
                    3. Rates; RA & DEC
                    *4. Apparent AZ & EL
                    5. Rates; AZ & EL
                    6. Sat. X & Y, pos. ang
                    7. Local app. sid. time
                    8. Airmass
                    9. Vis mag. & Surf Brt
                    10. Illuminated fraction
                    11. Defect of illumin.
                    12. Sat. angle separ/vis
                    13. Target angular diam.
                    14. Obs sub-lng & sub-lat
                    15. Sun sub-long & sub-lat
                    16. Sub Sun Pos. Ang & Dis
                    17. N. Pole Pos. Ang & Dis
                    18. Helio eclip. lon & lat
                    19. Helio range & rng rate
                    20. Obsrv range & rng rate
                    21. One-Way Light-Time
                    22. Speed wrt Sun & obsrvr
                    23. Sun-Obs-Targ ELONG ang
                    24. Sun-Targ-Obs PHASE ang
                    25. Targ-Obsrv-Moon/Illum
                    26. Obs-Primary-Targ angl
                    27. Pos. Ang;radius & -vel
                    28. Orbit plane angle
                    29. Constellation ID
                    30. Delta-T (CT - UT)
                    *31. Obs eclip. lon & lat
                    32. North pole RA & DEC
                    33. Galactic latitude
                    34. Local app. SOLAR time
                    35. Earth->Site lt-time
                    >36. RA & DEC uncertainty
                    >37. POS error ellipse
                    >38. POS uncertainty (RSS)
                    >39. Range & Rng-rate sig.
                    >40. Doppler/delay sigmas
                    41. True anomaly angle
                    42. Local app. hour angle
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
parser.add_argument('--out-units',
                    '-u',
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
parser.add_argument(
    '--csv',
    choices=['YES', 'NO'],
    help='toggles output of table in comma-separated value format')
parser.add_argument('--vec-labels',
                    '-l',
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
parser.add_argument('--output',
                    '-o',
                    default=sys.stdout,
                    help='specify the output filename')
parser.add_argument('--format',
                    default='ascii',
                    help='specify how the data table must be formatted')


def main():

    args = parser.parse_args()

    try:
        jplparams = read_config(filename=args.config)
    except ConfigNotFoundError:
        logger.warning('Configuration file not found.')
    except ConfigParserError:
        logger.error('Problems encountered while parsing configuration file.')

    jplparams.update({
        transform_key(k): v
        for k, v in vars(args).items()
        if is_jpl_param(k) and v
    })

    try:
        data = get(args.objs, dates=args.dates, **jplparams)
    except ConnectionError:
        logger.error('Connection error.')
        sys.exit(-1)
    except JplBadReqError as e:
        logger.error('Horizons says:\n\t' + e.__str__())
        sys.exit(-1)
    except ParserError:
        logger.error('''
        eph cannot parse this format.
        Try passing --csv YES option.
        ''')
        sys.exit(-1)

    try:
        data.write(args.output, format=args.format)
    except IOError:
        logger.error('Problems trying to write data.')
    # req = JplReq()
    #
    # try:
    # 	req.read(args.config)
    # except ConfigNotFoundError:
    # 	if args.config:
    # 		logger.error('Configuration file not found.')
    # 		sys.exit(-1)
    # 	elif args.suppress_warnings:
    # 		pass
    # 	else:
    # 		logger.warning('Configuration file not found.')
    # except ConfigParserError:
    # 	logger.error('Problems encountered while parsing configuration file.')
    # 	sys.exit(-1)
    #
    # req.set({
    # 	k: v for k, v in vars(args).items() if is_jpl_param(k) and v
    # })
    #
    # try:
    # 	res = req.query()
    # except ConnectionError:
    # 	logger.error('Connection error.')
    # 	sys.exit(-1)
    #
    # try:
    # 	if args.raw:
    # 		if args.ephem_only:
    # 			data = res.get_data()
    # 		else:
    # 			data = res.raw()
    # 	else:
    # 		data = res.parse()
    # except JplBadReqError as e:
    # 	logger.error('Horizons says:\n\t' + e.__str__())
    # 	sys.exit(-1)
    # except ParserError:
    # 	logger.error('''
    # 		eph cannot parse this format.
    # 		Try passing --csv YES option or --raw to get Horizons response as is.
    # 		''')
    # 	sys.exit(-1)
    #
    # try:
    # 	if isinstance(data, Table) and args.format:
    # 		data.write(args.output, format=args.format)
    # 	else:
    # 		if args.output is sys.stdout:
    # 			sys.stdout.write(data)
    # 		else:
    # 			with open(args.output, 'w') as f:
    # 				f.write(data)
    # except IOError:
    # 	logger.error('Problems trying to write data.')


if __name__ == '__main__':
    main()

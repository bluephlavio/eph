import argparse
import logging
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from ..config import read_config
from .jpl import JplReq, codify_obj, codify_site
from .shortcuts import get_table


COMMAND = 'jpl'
LOGGER = logging.getLogger()


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('start',
                        help='the start time date')
    parser.add_argument('stop',
                        help='the stop time date')
    parser.add_argument('object',
                        type=codify_obj,
                        help='the target object')
    parser.add_argument('--center', '-c',
                        type=codify_site,
                        help='the origin for the coordinate system')
    parser.add_argument('--step', '-s',
                        help='the time step between two data rows, or the number of steps')
    parser.add_argument('--ref-plane', '-p',
                        choices=['ECLIPTIC', 'FRAME', 'BODY_EQUATOR'],
                        help='the reference plane')
    parser.add_argument('--ref-system', '-r',
                        choices=['J2000', 'B1950'],
                        help='the reference system')
    parser.add_argument('--make-ephem',
                        action='store_true',
                        help='toggles generation of ephemeris, if possible')
    parser.add_argument('--table-type', '-t',
                        choices=['O', 'V', 'E', 'A'],
                        help='selects type of table to generate, if possible')
    parser.add_argument('--vec-table', '-v',
                        choices=[str(i) for i in range(1, 7)],
                        help='selects table format when --table-type=V')
    parser.add_argument('--units', '-u',
                        choices=['KM-S', 'AU-D', 'KM-D'],
                        help='selects output units when --table-type=V or --table-type=E')
    parser.add_argument('--csv',
                        action='store_true',
                        help='toggles output of table in comma-separated value format')
    parser.add_argument('--vec-label', '-l',
                        action='store_true',
                        help='toggles labelling of each vector component')
    parser.add_argument('--config',
                        help='the configuration file to be used')
    parser.add_argument('--output', '-o', help='the output filename')
    return parser


def read_defaults(config_file):
    config = read_config(config_file)
    return dict(config['jplparams'])


def load_request(args, defaults):

    req = JplReq(defaults).set({
        'start': args.start,
        'stop': args.stop,
        'object': args.object,
    })

    return req


def out(data, filename=None, **kwargs):
    if filename:
        data.write(filename, **kwargs)
    else:
        print(data)


def process(args):
    defaults = read_defaults(args.config)
    req = load_request(args, defaults)
    data = get_table(req)
    out(data, filename=args.output, format='ascii')


def main():
    try:
        parser = get_parser()
        args = parser.parse_args()
        process(args)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

import argparse
try:
    import configparser
except:
    import ConfigParser as configparser

from ..config import read_config
from .jpl import JplReq, codify_obj, codify_site


def init_req():
    config = read_config()
    jplparams = dict(config['jplparams'])
    return JplReq(jplparams)


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
                        choices=['O', 'VECTORS', 'E', 'A'],
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
    parser.add_argument('--output', '-o', help='the output filename')
    return parser


jpl_parser = get_parser()


def get_request(args):

    req = init_req()

    req.set({
        'start': args.start,
        'stop': args.stop,
        'object': args.object,
        'center': args.center or (req.center if 'center' in req.keys() else '@0'),
        'step': args.step or (req.step if 'step' in req.keys() else '2'),
        'ref_plane': args.ref_plane or (req.ref_plane if 'ref_plane' in req.keys() else 'BODY EQUATOR'),

    })

    return req


def jpl_process(args):

    req = get_request(args)
    res = req.query()
    data = res.get_table()

    if args.output:
        data.write(args.output, format='ascii')
    else:
        print(data)


def main():
    try:
        args = jpl_parser.parse_args()
        jpl_process(args)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

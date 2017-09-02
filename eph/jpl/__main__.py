import argparse
try:
    import configparser
except:
    import ConfigParser as configparser

from ..config import read_config
from .jpl import JplReq, codify_obj, codify_site


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('start')
    parser.add_argument('stop')
    parser.add_argument('object', type=codify_obj)
    parser.add_argument('--center', '-c', type=codify_site)
    parser.add_argument('--step', '-s')
    parser.add_argument('--output', '-o')
    return parser


jpl_parser = get_parser()


def get_request(args):

    config = read_config()
    defaults = dict(config['jplparams'])

    req = JplReq(defaults).set({
        'start': args.start,
        'stop': args.stop,
        'object': args.object,
    })

    if args.center:
        req.center = args.center
    if args.step:
        req.step = args.step

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
    args = jpl_parser.parse_args()
    jpl_process(args)


if __name__ == '__main__':
    main()

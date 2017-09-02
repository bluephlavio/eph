import argparse
try:
    import configparser
except:
    import ConfigParser as configparser

from eph.jpl.__main__ import jpl_parser, jpl_process


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('jpl', parents=[jpl_parser], add_help=False)
    return parser


eph_parser = get_parser()


def main():
    args = eph_parser.parse_args()
    if args.command == 'jpl':
       jpl_process(args)


if __name__ == '__main__':
    main()

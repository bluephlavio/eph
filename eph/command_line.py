import argparse
try:
    import configparser
except:
    import ConfigParser as configparser

import eph.jpl.command_line


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('jpl', parents=[eph.jpl.command_line.get_parser()], add_help=False)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.command == eph.jpl.command_line.COMMAND:
       eph.jpl.command_line.process(args)


if __name__ == '__main__':
    main()

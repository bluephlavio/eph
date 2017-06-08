import configparser, os, argparse
import eph
from eph.jpl import codify

def main():

    defaults = read_config()

    args = parse_args(defaults)

    req = eph.JplReq().set(defaults).set({
        'COMMAND': args.object,
        'START_TIME': args.start,
        'STOP_TIME': args.stop,
        'CENTER': args.center,
        'STEP_SIZE': args.step
        }
    )

    res = req.query()
    ephemeris = res.parse()
    write(ephemeris, filename=args.output)


def read_config():
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read([os.path.expanduser('~/.ephrc'), '.ephrc'])
    return dict(config.items('jplparams'))


def parse_args(defaults):
    parser = argparse.ArgumentParser()
    parser.add_argument('start')
    parser.add_argument('stop')
    parser.add_argument('object')
    parser.add_argument('--center', '-c', default=defaults.get('CENTER', 'sun'))
    parser.add_argument('--step', '-s', default=defaults.get('STEP_SIZE', '1d'))
    parser.add_argument('--output', '-o')
    args = parser.parse_args()

    args.object = codify(args.object)

    if args.center:
        args.center = codify(args.center, ref=True)

    return args


def write(ephemeris, filename=None):
    if filename:
        ephemeris.write(filename, format='ascii')
    else:
        print(ephemeris)



if __name__ == '__main__':
    main()




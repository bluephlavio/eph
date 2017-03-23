import configparser, os, argparse
import eph
from eph.jpl import name2code, name2refcode

def main():

	defaults = read_config()
	
	args = parse_args(defaults)

	req = eph.JPLReq().set(defaults).set({
		'START_TIME': args.start,
		'STOP_TIME': args.stop,
		'CENTER': args.center,
		'STEP_SIZE': args.step
		}
	)
	
	eph.Eph.join(
		*map(lambda x: req.set({'COMMAND': name2code(x)}).request().ephemeris, args.objects), 
		cols=args.cols,
		ids=args.ids
	).write(args.output)


def read_config():
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read([os.path.expanduser('~/.ephrc'), './.ephrc'])
	return dict(config.items('jplparams'))


def parse_args(defaults):
	parser = argparse.ArgumentParser()
	parser.add_argument('start')
	parser.add_argument('stop')
	parser.add_argument('objects', nargs='+')
	parser.add_argument('--center', '-c', default=defaults.get('CENTER', 'sun'))
	parser.add_argument('--step', '-s', default=defaults.get('STEP_SIZE', '1d'))
	parser.add_argument('--cols', nargs='+')
	parser.add_argument('--ids', nargs='+', default=(0,))
	parser.add_argument('--output', '-o')
	args = parser.parse_args()
	
	if args.center:
		args.center = name2refcode(args.center)
	
	if args.cols:
		args.cols = list(map(lambda x: int(x), args.cols))
	
	if args.ids:
		args.ids = tuple(map(lambda x: int(x), args.ids))
		
	return args



if __name__ == '__main__':
	main()
	


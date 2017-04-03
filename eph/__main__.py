import configparser, os, argparse, datetime, re
import eph
from eph.jpl import name2code, name2refcode

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():

	cfgs = read_config()
	defs = get_defaults(cfgs)
	args = parse_args(defs)
	ephs = fetch_data(args, defs)
	
	if args.subparser == 'get':
		get(ephs, args)
	elif args.subparser == 'plot':
		plot(ephs, args)


def read_config():
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read([os.path.expanduser('~/.ephrc'), './.ephrc'])
	return config


def get_defaults(config):
	return dict(config.items('jplparams'))


def parse_args(defaults):
	parser = argparse.ArgumentParser()
	
	subparsers = parser.add_subparsers(dest='subparser')
	
	get_parser = subparsers.add_parser('get')
	get_parser.add_argument('start')
	get_parser.add_argument('stop')
	get_parser.add_argument('objects', nargs='+')
	get_parser.add_argument('--step', '-s', default=defaults.get('STEP_SIZE', '1d'))
	get_parser.add_argument('--center', '-c', default=defaults.get('CENTER', 'sun'))
	get_parser.add_argument('--cols', nargs='+')
	get_parser.add_argument('--ids', nargs='+', default=())
	get_parser.add_argument('--output', '-o')
	
	plot_parser = subparsers.add_parser('plot')
	plot_parser.add_argument('start')
	plot_parser.add_argument('stop')
	plot_parser.add_argument('objects', nargs='+')
	plot_parser.add_argument('--step', '-s', default=defaults.get('STEP_SIZE', '1d'))
	plot_parser.add_argument('--center', '-c', default=defaults.get('CENTER', 'sun'))
	plot_parser.add_argument('--cols', nargs='+')
	plot_parser.add_argument('--dim', '-d', type=int, choices=[2,3], default=3)
	
	args = parser.parse_args()
	
	if args.center:
		args.center = name2refcode(args.center)
	
	if args.cols:
		args.cols = list(map(lambda x: int(x), args.cols))
	
	try:
		if args.ids:
			args.ids = tuple(map(lambda x: int(x), args.ids))
	except:
		pass
		
	return args


def fetch_data(args, defaults):
	start = args.start
	stop = args.stop
	step = args.step
	center = args.center
	
	single_date = False
	
	if stop == '.':
		single_date = True
		stop = datetime.datetime.strptime(args.start, '%Y-%m-%d')
		stop = stop.replace(day=stop.day+1).strftime('%Y-%m-%d')
	
	req = eph.JPLReq().set(defaults).set({
		'START_TIME': start,
		'STOP_TIME': stop,
		'STEP_SIZE': step,
		'CENTER': center,
		}
	)
	
	if single_date:
		return map(lambda x: eph.Eph(req.set({'COMMAND': name2code(x)}).request().ephemeris[0:1]), args.objects)
	
	return map(lambda x: req.set({'COMMAND': name2code(x)}).request().ephemeris, args.objects)


def get(ephs, args):
	eph.Eph.join(
		*ephs, 
		cols=args.cols,
		ids=args.ids
	).write(args.output)
	

def plot(ephs, args):
	fig = plt.figure()
	kwargs = {}
	if args.dim == 3:
		kwargs['projection'] = '3d'
	ax = fig.add_subplot('111', **kwargs)
	for ephemeris in ephs:
		eph.plot(ax, ephemeris, args.cols)
	plt.show()

if __name__ == '__main__':
	main()
	


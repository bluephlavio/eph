import configparser, os, argparse
import eph
#from eph import *

obj_code = {
	'sun': 0,
	'mercury': 199,
	'venus': 299,
	'earth': 399,
	'mars': 499,
	'jupyter': 599,
	'saturn': 699,
	'uranus': 799,
	'neptune': 899}

def main():
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read([os.path.expanduser('~/.ephrc'), './.ephrc'])
	defaults = dict(config.items('jplparams'))
	
	parser = argparse.ArgumentParser()
	parser.add_argument('start')
	parser.add_argument('stop')
	parser.add_argument('objects', nargs='+')
	parser.add_argument('--center', '-c', default=defaults.get('CENTER', 'sun'))
	parser.add_argument('--step', '-s', default=defaults.get('STEP_SIZE', '1d'))
	parser.add_argument('--cols', nargs='+')
	parser.add_argument('--ids', nargs='+')
	args = parser.parse_args()
	
	if args.center in obj_code:
		args.center = str(obj_code[args.center])
	
	args.center = "'@" + args.center + "'"
	
	if args.cols:
		args.cols = list(map(lambda x: int(x), args.cols))
	
	if args.ids:
		args.ids = tuple(map(lambda x: int(x), args.ids))
	else:
		args.ids = (0,)
	
	req = eph.JPLReq().set(defaults).set({
		'START_TIME': args.start,
		'STOP_TIME': args.stop,
		'CENTER': args.center,
		'STEP_SIZE': args.step})
	
	ephemerides = []
	
	for obj in args.objects:
		if obj in obj_code:
			obj = str(obj_code[obj])
				
		req.set({'COMMAND': obj})
		res = req.request()
		ephemerides.append(res.ephemeris)
	
	ephemeris = eph.Eph.join(*ephemerides, cols=args.cols, ids=args.ids)
	
	print(ephemeris)

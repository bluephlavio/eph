import sys, unittest
sys.path.append('../eph')
from eph.jpl import *

MINIMAL = {'COMMAND': "'399'", 'START_TIME': "'2016-01-01'", 'STOP_TIME': "'2017-01-01'"}
BASE_URL = 'http://ssd.jpl.nasa.gov/horizons_batch.cgi'
CONFIG_FILE = 'test/res/def.cfg'
SECTION = 'jplparams'

class TestJPLReq(unittest.TestCase):

	def setUp(self):
		self.req = JPLReq()
		
	def tearDown(self):
		del self.req
		
	def test_set(self):
		self.req.set({'key':'value'})
		self.assertEqual(self.req['key'], 'value')

	def test_read(self):
		self.req.read(CONFIG_FILE, SECTION)
		self.assertEqual(self.req['CENTER'], "'@0'")
		
	def test_url(self):
		self.req['key'] = 'value'
		url1 = BASE_URL + '?batch=1&key=value'
		url2 = BASE_URL + '?key=value&batch=1'
		self.assertTrue(self.req.url() in (url1, url2))
		
	def test_request(self):
		self.req.read(CONFIG_FILE, SECTION).set(MINIMAL)
		res = self.req.request()
		self.assertEqual(res.status, 200)
			
class TestJPLRes(unittest.TestCase):
	
	def setUp(self):
		self.bad_req = JPLReq()
		self.good_req = JPLReq().read(CONFIG_FILE, SECTION).set(MINIMAL)
			
	def tearDown(self):
		pass
		
	def test_init(self):
		good_res = self.good_req.request()
		self.assertEqual(good_res.status, 200)
		try:
			bad_res = self.bad_req.request()
			self.assertEqual(bad_res.status, 200)
		except BadRequestError as e:
			print(e)
			
	def test_parsejpl(self):
		res = self.good_req.request()
		self.assertTrue(res.ephemeris is not None)
			
if __name__ == '__main__':
	unittest.main()
	
	
	

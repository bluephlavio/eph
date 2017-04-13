import os, sys, datetime, requests, unittest
sys.path.append('../eph')
from eph.jpl import *



QUERY = {
    'COMMAND': '299',
    'START_TIME': '2007-11-17',
    'STOP_TIME': datetime.date.today().strftime('%Y-%m-%d')
}
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'res/def.cfg')
JPL_EPH_EXAMPLE = os.path.join(os.path.dirname(__file__), 'res/jpleph.txt')
JPL_URL_EXAMPLE = os.path.join(os.path.dirname(__file__), 'res/url.txt')



class TestJplReq(unittest.TestCase):


    def setUp(self):
        self.req = JplReq()


    def tearDown(self):
        del self.req


    def test_url(self):
        self.req.set({'key': 'value'})
        self.assertEqual(self.req.url(), 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&key=value')


    def test_query(self):
        self.req.read(CONFIG_FILE).set(QUERY)
        res = self.req.query().res
        self.assertEqual(res.status_code, 200)



class TestJplRes(unittest.TestCase):


    def test_parse(self):
        with open(JPL_URL_EXAMPLE, 'r') as f:
            urls = f.readlines()
            for url in urls:
                try:
                    res = JplRes(requests.get(url))
                    eph = res.parse()
                    self.assertTrue(True)
                except JplBadReq:
                    self.assertTrue(False)



class TestJplParser(unittest.TestCase):


    def test_parse(self):
        with open(JPL_EPH_EXAMPLE, 'r') as f:
            source = f.read()
            try:
                eph = JplParser().parse(source)
                self.assertTrue(True)
            except JplParserError:
                self.assertTrue(False)



class TestJplHelper(unittest.TestCase):


    def test_translate(self):
        self.assertEqual(translate('earth'), '399')
        self.assertEqual(translate('\'earth\''), '399')
        self.assertEqual(translate('399'), '399')
        self.assertEqual(translate('\'399\''), '399')
        self.assertEqual(translate('earth', ref=True), '\'@399\'')
        self.assertEqual(translate('\'earth\'', ref=True), '\'@399\'')
        self.assertEqual(translate('\'@earth\'', ref=True), '\'@399\'')
        self.assertEqual(translate('399', ref=True), '\'@399\'')
        self.assertEqual(translate('\'399\'', ref=True), '\'@399\'')
        self.assertEqual(translate('\'@399\'', ref=True), '\'@399\'')



if __name__ == '__main__':
    unittest.main()




import sys, unittest
sys.path.append('../eph')
from eph.util import *



class TestUtil(unittest.TestCase):

    def test_isvector(self):
        self.assertTrue(isvector([1,2,3]))
        self.assertFalse(isvector('abc'))
        self.assertFalse(isvector(0))


    def test_parsetable(self):
        self.assertEqual(parsetable('a, 1,\n b , 2,'), [['a', '1'], ['b', '2']])
        self.assertEqual(parsetable('a, 1,'), ['a', '1'])


    def test_numberify(self):
        self.assertEqual(numberify([['a', '1'], ['b', '2']]), [['a', 1.], ['b', 2.]])


    def test_transpose(self):
        self.assertEqual(transpose([['a', 'b'], ['1', '2']]), [['a', '1'], ['b', '2']])


    def test_addparams2url(self):
        self.assertEqual(addparams2url('http://xyz.com', {'key': 'value'}), 'http://xyz.com?key=value')
        self.assertEqual(addparams2url('http://xyz.com?', {'key': 'value'}), 'http://xyz.com?key=value')
        self.assertEqual(addparams2url('http://xyz.com?a=b', {'key': 'value'}), 'http://xyz.com?a=b&key=value')

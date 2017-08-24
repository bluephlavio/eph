from os import linesep
import sys
sys.path.append('..')

import unittest

from eph.jpl.models import BaseMap


class ConcreteMap(BaseMap):


    def __getattr__(self, key):
        return super().__getattr__(key)


    def __setattr__(self, key, value):
        super().__setattr__(key, value)


    def __delattr__(self, key):
        super().__delattr__(key)



class Testconcrete_map(unittest.TestCase):


    def setUp(self):
        self.concrete_map = ConcreteMap({'a': 1, 'b': 2}, c=3)


    def tearDown(self):
        del self.concrete_map


    def test_init(self):
        concrete_map = ConcreteMap()
        self.assertTrue(False if concrete_map else True)
        self.assertTrue(True if self.concrete_map else False)
        concrete_map = ConcreteMap({'a': 1}, b=2)
        self.assertEqual(concrete_map.a, 1)
        self.assertEqual(concrete_map['b'], 2)


    def test_set(self):
        self.concrete_map.set({'c' : 0}, d=0)
        self.assertEqual(self.concrete_map.c, 0)
        self.assertEqual(self.concrete_map.d, 0)


    def test_getattr(self):
        self.assertEqual(self.concrete_map.a, 1)


    def test_setattr(self):
        self.concrete_map.a = 0
        self.assertEqual(self.concrete_map.a, 0)


    def test_delattr(self):
        self.assertTrue('a' in self.concrete_map)
        self.assertTrue('b' in self.concrete_map)
        delattr(self.concrete_map, 'b')
        self.assertTrue('a' in self.concrete_map)
        self.assertTrue('b' not in self.concrete_map)


    def test_getitem(self):
        self.assertEqual(self.concrete_map['a'], 1)


    def test_setitem(self):
        self.concrete_map['a'] = 0
        self.assertEqual(self.concrete_map['a'], 0)


    def test_delitem(self):
        self.assertTrue('a' in self.concrete_map)
        self.assertTrue('b' in self.concrete_map)
        del self.concrete_map['b']
        self.assertTrue('a' in self.concrete_map)
        self.assertTrue('b' not in self.concrete_map)



if __name__ == '__main__':
    unittest.main()



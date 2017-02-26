import unittest
from eph.eph import *

class TestEph(unittest.TestCase):

	RAW = 'ciao, mondo\nhello, world\nsalam, aleikum'
	ROWS = RAW.splitlines()
	DIRTY_RAW = ' \n \n ciao, mondo\n\nhello , world, \n   salam, aleikum,\n \n'
	CLEAN_RAW = 'ciao,mondo\nhello,world\nsalam,aleikum'
	CLEAN_ROWS = CLEAN_RAW.splitlines()
	CLEAN_COLS = [len(row.split(',')) for row in CLEAN_ROWS]
	FILENAME = 'test/res/eph.txt'
	
	def setUp(self):
		self.dirty_eph = Eph.from_raw(TestEph.DIRTY_RAW)
		self.clean_eph = Eph.from_raw(TestEph.DIRTY_RAW).clean()
		
	def tearDown(self):
		pass
		
	def test_from_raw(self):
		self.assertEqual(Eph.from_raw(TestEph.RAW, delimiter=',').__str__(), TestEph.RAW)
		
	def test_from_rows(self):
		self.assertEqual(Eph.from_rows(TestEph.ROWS, delimiter=',').__str__(), TestEph.RAW)
		
	def test_from_file(self):
		self.assertEqual(Eph.from_file(TestEph.FILENAME, delimiter=',').__str__(), TestEph.RAW)
		
	def test_clean(self):
		self.assertEqual(self.clean_eph.__str__(), TestEph.CLEAN_RAW)
		
	def test_rows(self):
		self.assertEqual(self.clean_eph.rows(), TestEph.CLEAN_ROWS)
		
	def test_n_cols(self):
		self.assertEqual(self.clean_eph.n_cols(), TestEph.CLEAN_COLS)
		
	def test_is_valid(self):
		self.assertTrue(self.clean_eph.is_valid() and not self.dirty_eph.is_valid())
		
	def test_select_cols(self):
		self.assertEqual(self.clean_eph.select_cols(0).__str__(), 'ciao\nhello\nsalam')
		
	def test_join(self):
		joined_eph1 = Eph.join(self.clean_eph, self.clean_eph, cols=(0,1), ids=(0,))
		self.assertEqual(joined_eph1.__str__(), 'ciao,mondo,mondo\nhello,world,world\nsalam,aleikum,aleikum')
		joined_eph2 = Eph.join(self.clean_eph, self.clean_eph, cols=(1,), ids=())
		self.assertEqual(joined_eph2.__str__(), 'mondo,mondo\nworld,world\naleikum,aleikum')
		joined_eph3 = Eph.join(self.clean_eph, self.clean_eph, cols=(0,1), ids=())
		self.assertEqual(joined_eph3.__str__(), 'ciao,mondo,ciao,mondo\nhello,world,hello,world\nsalam,aleikum,salam,aleikum')

if __name__ == '__main__':
	unittest.main()



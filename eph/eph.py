"""
Define base class :class:`Eph`. :class:`Eph` class is fundamental to this package because it represents an ephemeris, allowing manipulation of this kind of data structures.
"""

import os, re, statistics

class Eph(list):
	"""
	Base class for manipulating and combining ephemerides.

	* An :class:`Eph` object is a :class:`list` of rows containing data.
	* Rows are expected to be :class:`list` of data cells.
	* Data cells can be either strings or any type.

	:class:`Eph` objects can be created with some *class methods*:

	* from a :class:`list` of strings interpreted as rows containing strings of data.
	* from a raw string containing all rows of data.
	* from a csv-like data file.

	An :class:`Eph` object is considered *valid* if all rows have the same length or, said otherwise, if all rows of data have the same number of columns.
	An :class:`Eph` is considered *clean* if does not contain useless spaces in data cells, empty rows or empty columns.

	A new :class:`Eph` object can be obtained selecting columns from one :class:`Eph` object or combining specific columns of many :class:`Eph` objects.
	"""
	
	def __init__(self, *args, **kwargs):
		"""Constructs an :class:`Eph` object from list of lists of data cells.
		
		:param args: passed to :class:`list` ``__init__`` method.
		:param kwargs: use ``delimiter`` key to set delimiter character between columns.
		"""
		list.__init__(self, *args)
		self.delimiter = kwargs.get('delimiter', ',')
		#self.clean()
		
	@classmethod
	def from_rows(cls, rows, **kwargs):
		"""Creates an :class:`Eph` object from a :class:`list` of string type rows.
		
		:param rows: the :class:`list` of rows.
		:type rows: :class:`list`
		:param kwargs: use ``delimiter`` key to set delimiter character between columns.
		"""
		delimiter = kwargs.get('delimiter', ',')
		return cls(map(lambda row: row.split(delimiter), rows), **kwargs)
		
	@classmethod
	def from_raw(cls, raw, **kwargs):
		"""Creates an :class:`Eph` object from a raw text ephemeris.
		
		:param raw: the string to be interpreted as an ephemeris.
		:type raw: :class:`str`
		:param kwargs: use ``delimiter`` key to set delimiter character between columns.
		"""
		return cls.from_rows(raw.splitlines(), **kwargs)
		
	@classmethod
	def from_file(cls, filename, **kwargs):
		"""Creates an :class:`Eph` object from a ephemeris text file.
		
		:param filename: the file containing the ephemeris data.
		:type filename: :class:`str`
		:param kwargs: use ``delimiter`` key to set delimiter character between columns.
		"""
		raw = open(filename, 'r').read()
		return cls.from_raw(raw, **kwargs)
		
	def __str__(self):
		"""Produces a human readable ephemeris string."""
		return os.linesep.join(self.rows())
		
	def clean(self):
		"""Cleans the ephemeris.
		
		An :class:`Eph` is considered *clean* if does not contain useless spaces in data cells, empty rows or empty columns.

		:return: the object itself.
		:rtype: :class:`Eph`
		"""
		for i, row in enumerate(self):
			for j, col in enumerate(row):
				row[j] = re.sub(r'^\s*|\s*$', '', col)
			if len(row):
				if not row[-1]:
					del row[-1]
		garbage = []
		for i, row in enumerate(self):
			if not row:
				garbage.append(i)
		for i in reversed(garbage):
			del self[i]
		return self
		
	def rows(self):
		"""Gives a :class:`list` of string type formatted rows.
		
		:return: the :class:`list` of rows.
		:rtype: :class:`list`
		"""
		return [self.delimiter.join(row) for row in self]
	
	def n_cols(self):
		"""Gives the number of columns for each row.
		
		:return: a :class:`list` of integers representing the number of columns for all rows.
		:rtype: :class:`list`
		"""
		return [len(row) for row in self]
		
	def is_valid(self):
		"""Check if :class:`Eph` object can be considered a *valid* representation of an ephemeris.
		
		An :class:`Eph` object is considered *valid* if all rows have the same length or, said otherwise, if all rows of data have the same number of columns.
		"""
		return statistics.pvariance(self.n_cols()) == 0
		
	def is_empty(self):
		"""Tells if the ephemeris has zero rows or not."""
		if len(self):
			return False
		else:
			return True
	
	def select_cols(self, *cols):
		"""Creates an :class:`Eph` object from the columns specified with their indices.
		
		:param cols: indices of columns to be selected.
		:type cols: :class:`list`
		
		:return: the :class:`Eph` object built from the columns specified.
		:rtype: :class:`Eph`
		"""
		try:
			eph = Eph([[row[i] for i in cols] for row in self], delimiter = self.delimiter)
		except IndexError:
			eph = Eph([])
		finally:
			return eph
	
	@staticmethod
	def join(*ephs, cols=None, ids=()):
		"""Combines many :class:`Eph` objects.
		
		:param ephs: :class:`Eph` objects to join.
		:type ephs: :class:`Eph`
		
		:param cols: a :class:`list` of columns to select for each :class:`Eph` object.
		:type cols: :class:`list`
		
		:param ids: a :class:`tuple` of indices that identify columns that will be treated as *ids*. A column is considered an *id* if values are equal for all ephemerides to join and it will present only once in the resulting ephemeris.
		:type ids: :class:`tuple`
		
		:return: The :class:`Eph` object obtained combining multiple :class:`Eph` objects.
		:rtype: :class:`Eph`
		"""
		if cols == None:
			if len(ephs):
				cols = list(range(min(ephs[0].n_cols())))
			else:
				cols = ()
		cols = list(filter(lambda i: i not in ids, cols))
		ephslist = list(map(lambda eph: eph.select_cols(*cols), ephs))
		ephslist = list(filter(lambda eph: not eph.is_empty(), ephslist))
		if len(ephs) and len(ids):
			ephslist.insert(0, ephs[0].select_cols(*ids))
		return Eph.from_rows([','.join(row) for row in zip(*map(lambda eph: eph.rows(), ephslist))])



"""
Define classes used to retrive a desired ephemris from JPL Horizon's service.

* :class:`JPLReq` represents a request to JPL Horizon's service. :class:`JPLReq` is a ``dict`` where key-values pairs are parameters accepted by JPL Horizon's interface (a complete description of the interface can be found at ftp://ssd.jpl.nasa.gov/pub/ssd/horizons_batch_example.long).
* :class:`JPLRes` represents a response by JPL Horizon's service. It gives a structure to ``http`` response by separating raw data in *header*, *ephemeris* and *footer*. :class:`JPLRes`.eph is parsed from ``http`` response as an :class:`Eph` object. :class:`JPLRes`.header and :class:`JPLRes`.footer are raw strings.
* :class:`BadRequestError` is a exception raised if the JPL Horizon's response is not formatted as expected, indicating that something went wrong (for example if :class:`JPLReq` parameters are not accepted by JPL Horizon's interface).
"""

import configparser, re
from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qs
import requests
from .eph import Eph

class JPLReq(dict):
	"""
	:class:`JPLReq` represents a request to JPL Horizons service. :class:`JPLReq` is a ``dict`` where key-values pairs are parameters accepted by JPL Horizons interface (a complete description of the interface can be found at ftp://ssd.jpl.nasa.gov/pub/ssd/horizons_batch_example.long).
	"""

	BASE_URL = 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1'

	def __init__(self, filename=None, params=None):
		"""
		Initializes a :class:`JPLReq` object from a ``dict``.
		
		:param params: key-value pairs of JPL parameters.
		:type params: ``dict``
		"""
		dict.__init__(self)
		if filename:
			self.read(*filename)
		if params:
			self.set(params)

	def set(self, params):
		"""
		Wrapper for ``dict``.update() allowing chaining.
		
		:param params: key-value pairs of JPL parameters.
		:type params: ``dict``
		:return: the object itself.
		:rtype: :class:`JPLReq`
		"""
		for key, value in params.items():
			self[key] = value
		return self

	def read(self, filename, section):
		"""
		Reads key-value pairs from file.
		
		:param filename: the filename to be parsed.
		:type filename: ``str``
		:param section: section of the ini file to be read.
		:type section: ``str``
		
		:return: the object itself.
		:rtype: :class:`JPLReq`
		"""
		cp = configparser.ConfigParser()
		cp.optionxform = str
		cp.read(filename)
		self.update(dict(cp.items(section)))
		return self
		
	def url(self):
		"""
		Builds a url addressing JPL Horizons service with query string specifying JPL params.
		
		:return: the url.
		:rtype: ``str``
		"""
		scheme, netloc, path, query, fragment = urlsplit(JPLReq.BASE_URL)
		query_dict = parse_qs(query)
		query_dict.update(self)
		query = urlencode(query_dict, doseq=True)
		return urlunsplit((scheme, netloc, path, query, fragment))
		
	def request(self):
		"""Make a request to JPL Horizons service server from the parameters assigned to it.
		
		:return: a :class:`JPLRes` object representing a structured version of raw ``http`` JPL response.
		:rtype: :class:`JPLRes`
		"""
		res = requests.get(self.url())
		return JPLRes(res)

class JPLRes:
	"""
	:class:`JPLRes` represents a response by JPL Horizon's service. It structures the raw ``http`` JPL response by separating data in *header*, *ephemeris* and *footer*. ``JPLRes.ephemeris`` is parsed from ``http`` response as an :class:`Eph` object. ``JPLRes.header`` and ``JPLRes.footer`` are raw strings instead.
	"""
	
	def __init__(self, res=None):
		"""
		Creates an :class:`JPLRes` object from an ``http`` response from JPL Horizons service.

		:param res: the JPL Horizons response.
		:type res: ``requests.models.Response``
		"""
		if res:
			self.parsejpl(res)
			
	def parsejpl(self, res):
		"""
		Parses a JPL response and extracts three sections:
		
		* *header*: the header containing info about the requested celestial objects and the formatting of the ephemeris,
		* *ephemeris*: the actual data parsed as an :class:`Eph` object,
		* *footer*: the footer containing info about how things are to be intended, JPL Horizons service and the request's parameters used.

		:param res: the JPL Horizons response.
		:type res: ``requests.models.Response``

		:return: the object itself.
		:rtype: :class:`JPLRes`
		"""
		self.status = res.status_code
		self.all = res.text
		m = re.search('([\s\S]*)\$\$SOE([\s\S]*)\$\$EOE([\s\S]*)', self.all)
		if m is None:
			raise BadRequestError(self.all)
		else:
			self.header = m.group(1)
			self.ephemeris = Eph.from_raw(m.group(2)).clean()
			self.footer = m.group(3)
		return self
			
	def __str__(self):
		"""The entire JPL output."""
		return self.all
		

class BadRequestError(Exception):
	"""
	Exception raised when JPL output is not formatted as expected, indicating that something went wrong (probably because of an invalid param passed to the request).
	"""

	def __init__(self, jpl_msg):
		"""
		Creates a ``BadRequestError`` exception.

		:param jpl_msg: the JPL error message.
		:type jpl_msg: ``str``
		"""
		super().__init__(self, BadRequestError.__name__)
		self.jpl_msg = jpl_msg
		
	def __str__(self):
		"""The string representation of the exception."""
		return BadRequestError.__name__ + '! JPL Horizons says:\n\n' + self.jpl_msg



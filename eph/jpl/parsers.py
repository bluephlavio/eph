import abc
import re

from astropy.table import Table

from ..util import parse_table, numberify, transpose
from .exceptions import JplParserError



class BaseParser(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse(self, source):
        pass



class JplParser(BaseParser):


    EPH_REGEX = r'(?<=\$\$SOE\s)[\s\S]*?(?=\s\$\$EOE)'
    COL_NAMES_REGEX = r'(?<=\*[\r\n])[^\r\n]*(?=[\r\n]\*+\s\$\$SOE)'


    def __init__(self):
        self._delimiter = r'\s+'


    def parse(self, source):
        match = re.search(r'CSV_FORMAT\s=\s(\w+)', source)
        if match and match.group(1) == 'YES':
            self._delimiter = ','
        data = self.data(source)
        cols = self.cols(source)
        return Table(data, names=cols)


    def data(self, source):
        match = re.search(JplParser.EPH_REGEX, source)
        if match:
            return transpose(numberify(parsetable(match.group(), delimiter=self._delimiter)))
        else:
            raise JplParserError


    def cols(self, source):
        match = re.search(JplParser.COL_NAMES_REGEX, source)
        if match:
            return tuple(parsetable(match.group(), delimiter=self._delimiter))
        else:
            raise JplParserError





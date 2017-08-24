""" exceptions.py

Defines Jpl Horizons related exceptions.

"""

class JplError(Exception):
    pass



class JplParserError(JplError):
    pass



class JplBadReq(JplError):
    pass

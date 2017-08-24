from .jpl import JplReq


def getraw(req):
    if not isinstance(req, JplReq):
        raise ValueError
    res = req.query()
    return res.get_raw()


def gettable(req):
    if not isinstance(req, JplReq):
        raise ValueError
    res = req.query()
    return res.get_table()

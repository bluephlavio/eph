from .jpl import JplReq


def get_raw(req):
    if not isinstance(req, JplReq):
        raise ValueError
    res = req.query()
    return res.get_raw()


def get_table(req):
    if not isinstance(req, JplReq):
        raise ValueError
    res = req.query()
    return res.get_table()

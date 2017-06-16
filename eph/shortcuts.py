


def getraw(req):
    res = req.query()
    return res.get_raw()


def gettable(req):
    res = req.query()
    return res.get_table()

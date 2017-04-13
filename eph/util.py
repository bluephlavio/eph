import copy
from urllib.parse import urlparse, urlunparse, urlencode



def isvector(obj):
    return hasattr(obj, '__iter__') and not isinstance(obj, str)


def parsetable(raw, delimiter=','):
    tostrip = ' ' + delimiter
    data = raw.strip(tostrip).split('\n')
    for i, row in enumerate(data):
        data[i] = list(map(lambda x: x.strip(' '), row.strip(tostrip).split(delimiter)))
    if len(data) > 1:
        return data
    else:
        return data[0]


def numberify(data):
    numberified = copy.deepcopy(data)
    for i, obj in enumerate(numberified):
        if isvector(obj):
            numberified[i] = numberify(obj)
        else:
            try:
                numberified[i] = float(obj)
            except:
                pass
    return numberified


def transpose(data):
    return [list(row) for row in zip(*data)]


def addparams2url(url, params):
    if urlparse(url).query:
        return url + '&' + urlencode(params)
    else:
        return urlunparse(urlparse(url)) + '?' + urlencode(params)





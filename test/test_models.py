from eph.models import BaseMap


class ConcreteMap(BaseMap):

    def __getattr__(self, key):
        return super(self.__class__, self).__getattr__(key)

    def __setattr__(self, key, value):
        super(self.__class__, self).__setattr__(key, value)

    def __delattr__(self, key):
        super(self.__class__, self).__delattr__(key)


def test_map_model():
    map = ConcreteMap({'a': 1}, b=2)
    assert map.a == 1
    assert map['a'] == 1
    assert map.b == 2
    assert map['b'] == 2
    map.set({'a': 0, 'b': 1}, c=2)
    assert map.a == 0
    assert map['a'] == 0
    assert map.b == 1
    assert map['b'] == 1
    assert map.c == 2
    assert map['c'] == 2
    map.a = -1
    map['c'] = 0
    assert map.a == -1
    assert map['a'] == -1
    assert map.b == 1
    assert map['b'] == 1
    assert map.c == 0
    assert map['c'] == 0

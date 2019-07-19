import abc
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping


class BaseMap(MutableMapping):

    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        self.set(*args, **kwargs)

    @abc.abstractmethod
    def __getattr__(self, key):
        return self.__dict__[key]

    @abc.abstractmethod
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    @abc.abstractmethod
    def __delattr__(self, key):
        del self.__dict__[key]

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        self.__delattr__(key)

    def __iter__(self):
        return self.__dict__.__iter__()

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return self.__class__.__name__ + '(' + self.__dict__.__repr__() + ')'

    def __str__(self):
        return '\n'.join('{key}={value}'.format(key=k, value=v)
                         for k, v in self.__dict__.items())

    def set(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError(
                    'You can pass only one positional argument to set method.')
            else:
                arg = args[0]
                for k, v in arg.items():
                    self.__setattr__(k, v)
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        return self

class dump(type):

    def __print_wrapper(fun, name):
        def wrapper(self, *args, **kwargs):
            print(name, ': ', args,', ' , kwargs, sep='')
            return fun(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def __new__(metacls, name, parents, ns, **kwds):
        cls = super().__new__(metacls, name, parents, ns, **kwds)
        for name in cls.__dict__:
            obj = getattr(cls, name)
            if callable(obj):
                setattr(cls, name, dump.__print_wrapper(obj, name))
        return cls


import sys
exec(sys.stdin.read())
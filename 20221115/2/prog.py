class Num:
    def __set__(self, obj, val):
        if 'real' in dir(val):
            obj._data = val
        elif '__len__' in dir(val):
            obj._data = len(val)

    def __get__(self, obj, cls):
        if '_data' in obj.__dict__:
            return obj._data
        else:
            return 0

import sys
exec(sys.stdin.read())
class Alpha:
    __slots__ = [chr(x) for x in range(ord('a'), ord('z') + 1)]

    def __init__(self, **kwargs):
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    def __str__(self):
        result_str = []

        for attr in self.__slots__:
            try:
                val = getattr(self, attr)
            except AttributeError:
                continue
            else:
                result_str.append(f'{attr}: {val}')

        return ', '.join(result_str)

class AlphaQ:
    def __init__(self, **kwargs):
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    def __setattr__(self, name, val):
        if len(name) == 1 and ord(name) >= ord('a') and ord(name) <= ord('z'):
            self.__dict__[name] = val
        else:
            raise AttributeError

    def __str__(self):
        result_str = []

        for attr in (chr(x) for x in range(ord('a'), ord('z') + 1) if chr(x) in self.__dict__):
            result_str.append(f'{attr}: {getattr(self, attr)}')

        return ', '.join(result_str)


import sys
exec(sys.stdin.read())

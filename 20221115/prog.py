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


import sys
exec(sys.stdin.read())

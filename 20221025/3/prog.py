import itertools
print(*sorted(filter(lambda s: s.count("TOR") == 2, map(lambda s: ''.join(s), itertools.product("TOR", repeat=int(input()))))), sep=', ')
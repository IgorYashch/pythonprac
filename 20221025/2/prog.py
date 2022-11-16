import itertools

def slide(seq, n):
    seq = iter(seq)

    seq, curr = itertools.tee(seq, 2)
    yield from itertools.islice(curr, n)


    while next(seq, None) is not None:
        seq, curr = itertools.tee(seq, 2)
        yield from itertools.islice(curr, n)

import sys
exec(sys.stdin.read())
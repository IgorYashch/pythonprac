from functools import reduce

class Grange:

    seq = None
    start = None
    q = None
    end = None

    def __init__(self, start, q, end):    
        curr = start
        self.seq = []
        self.start = start
        self.end = end 
        self.q = q

        while (curr < end):
            self.seq.append(curr)
            curr *= q

    def __len__(self):
        return len(self.seq)

    def __bool__(self):
        return bool(self.seq)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return Grange(idx.start, self.q ** (idx.step or 1), idx.stop)
        elif idx < len(self.seq):
            return self.seq[idx]
        else:
            return self.start * self.q ** idx

    def __iter__(self):
        return iter(self.seq)

    def __repr__(self):
        return f'grange({self.start}, {self.q}, {self.end})'


import sys
exec(sys.stdin.read())
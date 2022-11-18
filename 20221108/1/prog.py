from collections import UserString

class DivStr(UserString):
    def __init__(self, val=""):
        super().__init__(val)
        # else:
        #     super().__init__("none")
        #     self.data = ""
        # pass

    def __floordiv__(self, other):
        k = len(self.data) // other
        return iter(self.data[i: i + k] for i in range(0, k * other, k))

    def __mod__(self, other):
        l = len(self.data) % other
        return DivStr(self.data[-l:] if l else "")

import sys
exec(sys.stdin.read())
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

class Triangle:
    
    t1 = t2 = t3 = None
    
    def __init__(self, t1, t2, t3):
        self.t1 = Point(*t1)
        self.t2 = Point(*t2)
        self.t3 = Point(*t3)

    def __bool__(self):
        return abs(self) != 0

    def __abs__(self):
        return 1 / 2 * abs(self.t1.x * (self.t2.y - self.t3.y) +\
                           self.t2.x * (self.t3.y - self.t1.y) +\
                           self.t3.x * (self.t1.y - self.t2.y)
                          )

    def __lt__(self, other):
        return abs(self) < abs(other)

    def contains_point(self, point):

            sub_area1 = abs(Triangle(point, self.t1, self.t2))
            sub_area2 = abs(Triangle(point, self.t1, self.t3))
            sub_area3 = abs(Triangle(point, self.t2, self.t3))

            return sub_area1 + sub_area2 + sub_area3 == abs(self)

    def __contains__(self, other):
        if not other:
            return True

        return self.contains_point(other.t1) and\
               self.contains_point(other.t2) and\
               self.contains_point(other.t3)

    def __and__(self, other):
        if not self or not other:
            return False

        return self.contains_point(other.t1) or\
               self.contains_point(other.t2) or\
               self.contains_point(other.t3) or\
               other.contains_point(self.t1) or\
               other.contains_point(self.t2) or\
               other.contains_point(self.t3)

import sys
exec(sys.stdin.read())
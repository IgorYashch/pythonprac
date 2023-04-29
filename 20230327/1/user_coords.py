class Coordinates:
    def __init__(self, x, y, map_size):
        self.data = (x, y)
        self.map_size = map_size

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__((self.data[0] + other.data[0]) % self.map_size[0],
                          (self.data[1] + other.data[1]) % self.map_size[1],
                          self.map_size)
        elif isinstance(other, tuple):
            return self.__class__((self.data[0] + other[0]) % self.map_size[0],
                          (self.data[1] + other[1]) % self.map_size[1],
                          self.map_size)
        else:
            raise TypeError("Something wrong with this operation")
        
    def __eq__(self, other):
        return self.data == other.data

    def __repr__(self):
        return f"({self.data[0]}, {self.data[1]})"
    
    def __hash__(self):
        return hash(self.data)
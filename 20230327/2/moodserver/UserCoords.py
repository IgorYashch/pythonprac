"""Module for coordinates class."""


class Coordinates:
    """Class of coordinates for the MUD game."""
    def __init__(self, x, y, map_size):
        """Initialize the coordinates with given x, y and map size."""
        self.data = (x, y)
        self.map_size = map_size

    def __add__(self, other):
        """Add two coordinate objects or a coordinate object and a tuple."""
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
        """Check if two coordinate objects are equal."""
        return self.data == other.data

    def __repr__(self):
        """Return a string representation of the coordinates."""
        return f"({self.data[0]}, {self.data[1]})"

    def __hash__(self):
        """Compute the hash value of the coordinates."""
        return hash(self.data)

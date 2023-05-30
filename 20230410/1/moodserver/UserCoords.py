"""Модуль для класса координат."""


class Coordinates:
    """
    Класс координат для игры MUD.
    """
    def __init__(self, x, y, map_size):
        """
        Инициализирует координаты с заданными x, y и размером карты.

        :param x: Координата x.
        :type x: int
        :param y: Координата y.
        :type y: int
        :param map_size: Размер карты.
        :type map_size: tuple
        """
        self.data = (x, y)
        self.map_size = map_size

    def __add__(self, other):
        """
        Складывает два объекта координат или объект координат и кортеж.

        :param other: Другой объект координат или кортеж.
        :type other: Coordinates or tuple
        :return: Результат сложения координат.
        :rtype: Coordinates
        :raises TypeError: Если тип other не поддерживается.
        """
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
        """
        Проверяет равенство двух объектов координат.

        :param other: Другой объект координат для сравнения.
        :type other: Coordinates
        :return: Результат сравнения.
        :rtype: bool
        """
        return self.data == other.data

    def __repr__(self):
        """
        Возвращает строковое представление координат.

        :return: Строковое представление координат.
        :rtype: str
        """
        return f"({self.data[0]}, {self.data[1]})"

    def __hash__(self):
        """
        Вычисляет хэш-значение координат.

        :return: Хэш-значение координат.
        :rtype: int
        """
        return hash(self.data)

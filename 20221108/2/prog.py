from functools import reduce

class InvalidInput(Exception): pass

class BadTriangle(Exception): pass

def triangleSquare(s):
    # Считывание с проверкой
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(s)
    except Exception:
        raise InvalidInput

    # Проверка на числовой формат
    def check_numeric(x):
        return type(x) == int or type(x) == float

    if not reduce(lambda x,y: x and y, [check_numeric(x) for x in [x1,x2,x3,y1,y2,y3]]):
        raise BadTriangle

    # Проверяем, что точки не лежат на одной прямой
    def area(t1, t2, t3):
        return 1 / 2 * abs(t1[0] * (t2[1] - t3[1]) +\
                           t2[0] * (t3[1] - t1[1]) +\
                           t3[0] * (t1[1] - t2[1])
                          )

    # Вычисляем площадь
    s = area((x1, y1), (x2, y2), (x3, y3))

    if s:
        return s
    else:
        raise BadTriangle


while True:
    try:
        s = triangleSquare(input())
    except BadTriangle:
        print("Not a triangle")
    except InvalidInput:
        print("Invalid input")
    else:
        print('{:.2f}'.format(s))
        break

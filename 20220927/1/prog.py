print([x for x in range(*eval(input())) if all(x % i for i in range(2, x // 2 + 1)) and x != 1])
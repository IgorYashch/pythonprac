def Pareto(*pairs):
    result = []
    for i, (x, y) in enumerate(pairs):
        for a, b in [p for j, p in enumerate(pairs) if j != i]:
            if (x <= a and y < b) or (x < a and y <= b):
                break
        else:
            result.append((x, y))
    return tuple(result)

print(Pareto(*eval(input())))
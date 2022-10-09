def sub(x, y):

    if type(x) is tuple or type(x) is list:
        return type(x)([a for a in x if a not in y])
    else:
        return x - y

print(sub(*eval(input())))
from math import * 

def Calc(s, t, u):
    def func(x):
        tmp = eval(s)
        y = eval(t)
        x = tmp
        return eval(u)
    return func

a, b, c = eval(input())

n = eval(input())

print(Calc(a, b, c)(n))
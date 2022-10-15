from math import *

def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num

inpt = input().split()

w, h = map(int, inpt[:2])
a, b = map(float, inpt[2:4])
expr = inpt[-1]

w_step = (b - a) / (w - 1)

expr_vals = []
for i in range(w):
    x = a + w_step * i
    expr_vals += [eval(expr)]

max_f, min_f = max(expr_vals), min(expr_vals)

map_ = [[' '] * w for i in range(h)]
indexes_for_colums = []

for j in range(w):
    i = int_r((expr_vals[j] - min_f) / (max_f - min_f)* h)
    if i == h:
        i = h - 1

    map_[-i - 1][j] = '*'
    indexes_for_colums.append(-i - 1)

for j in range(1, w):
    k, n = indexes_for_colums[j - 1: j + 1]
    if n < k:
        for l in range(n + 1, k):
            map_[l][j] = '*'
    else:
        for l in range(k + 1, n):
            map_[l][j - 1] = '*'

print('\n'.join([''.join(s) for s in map_]))
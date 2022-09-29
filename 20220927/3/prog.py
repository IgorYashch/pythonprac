input_ = []

while s := input():
    input_.append(list(eval(s)))

# предполагаем, что ввод всегда полностью корректный

n = len(input_)//2

a = input_[: n]
b = input_[n:]


mul = []

for i in range(n):
    mul.append([])
    for j in range(n):
        mul[-1].append(sum([x * y for x, y in zip(a[i], [b[k][j] for k in range(n)])]))

for x in mul:
    print(','.join(str(a) for a in x))
first_line = list(eval(input()))
n = len(first_line)
input_ = [first_line]

for i in range(2 * n - 1):
    input_.append(list(eval(input())))


# предполагаем, что ввод всегда полностью корректный

a = input_[: n]
b = input_[n:]

mul = []

for i in range(n):
    mul.append([])
    for j in range(n):
        mul[-1].append(sum([x * y for x, y in zip(a[i], [b[k][j] for k in range(n)])]))

for x in mul:
    print(','.join(str(a) for a in x))
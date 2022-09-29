l = list(eval(input()))

key = lambda x: x ** 2 % 100

for i in range(len(l) - 1):
    for j in range(i + 1, len(l)):
        if key(l[i]) > key(l[j]):
            l[i], l[j] = l[j], l[i]

print(l)
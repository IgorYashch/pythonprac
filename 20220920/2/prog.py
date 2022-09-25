s = 0

while (x := int(input())) > 0:
    s += x

    if s > 21:
        print(s)
        break
else:
    print(x)
n = int(input())

def digits_sum(x):
    s = 0
    while x:
        x, digit = divmod(x, 10)
        s += digit
    return s


k = 0
while k < 3:
    l = 0
    while l < 2:
        mul = (n + k) * (n + l)
        print('{} * {} = {}'.format(n + k, n + l, mul if digits_sum(mul) != 6 else ':=)'), end = ' ')
        l += 1
    else:
        mul = (n + k) * (n + l)
        print('{} * {} = {}'.format(n + k, n + l, mul if digits_sum(mul) != 6 else ':=)'))
    k += 1
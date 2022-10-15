from fractions import Fraction

s, w, *pows_and_coeffs = input().split(', ')
s, w = Fraction(s), Fraction(w)

pow_a = int(pows_and_coeffs.pop(0))
coeffs_a = list(map(Fraction, pows_and_coeffs[:pow_a + 1]))
del pows_and_coeffs[:pow_a + 1]
pow_b = int(pows_and_coeffs.pop(0))
coeffs_b = list(map(Fraction, pows_and_coeffs))

def check(pln_a, pln_b, s, w):
    fa = lambda x: sum([coeff * x ** i for i, coeff in enumerate(pln_a[::-1])])
    fb = lambda x: sum([coeff * x ** i for i, coeff in enumerate(pln_b[::-1])])

    if fb(s) == 0:
        return False
    else:
        return fa(s) / fb(s) == w


print(check(coeffs_a, coeffs_b, s, w))
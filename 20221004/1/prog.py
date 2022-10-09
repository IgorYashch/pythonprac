def binary_search(elem, seq):
    n = len(seq)
    center = n // 2 - (1 if n % 2 == 0else 0)

    if not seq:
        return False

    if seq[center] == elem:
        return True
    elif elem < seq[center]:
        return binary_search(elem, seq[:center])
    else:
        return binary_search(elem, seq[center + 1:])

print(binary_search(*eval(input())))
from collections import Counter

counter = Counter()

w = int(input())


while s := input():
    words = ''.join([c if c.isalpha() else ' ' for c in s.lower()]).split()
    counter.update(filter(lambda x: len(x) == w, words))

l = counter.most_common()
if l:
    max_count = l[0][1]
    print(' '.join(sorted([x for x, count in l if count == max_count])))

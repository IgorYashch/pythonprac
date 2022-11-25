<<<<<<< HEAD
import sys

s = sys.stdin.buffer.read()
n = int(s[0])
blocks = []

curr_pos = 1



for i in range(1, n + 1):
    size = int(i * (len(s) - curr_pos) / n)
    blocks.append(s[curr_pos:curr_pos + size])
    curr_pos += size

print(s[:1] + b''.join(sorted(blocks)))
=======
# Просто чтобы отметиться на семинаре
>>>>>>> cf9c27b75bd136d6e0f20ff0e10b3b1505f00215

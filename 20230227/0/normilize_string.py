import shlex
import readline

while s := input():
    norm_s = shlex.join(shlex.split(s))
    if norm_s == 'quit':
        break
    print(norm_s)

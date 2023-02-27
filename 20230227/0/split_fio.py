import shlex
import readline

fio = input()
address = input()
line = shlex.join(['register', fio, address])
print(line)
print(shlex.split(line))

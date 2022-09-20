x = int(input())

checker = ['-'] * 3
if x % 25 == 0:
  if x % 2 == 0:
    checker[0] = '+'
  else:
    checker[1] = '+'
if x % 8 == 0:
  checker[2] = '+'

print("A {} B {} C {}".format(*checker))
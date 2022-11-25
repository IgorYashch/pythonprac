import sys 
s = sys.stdin.buffer.read()
print(s.decode('UTF8', errors='replace')\
       .encode('latin1', errors='replace')\
       .decode('cp1251', errors='replace')
     )
import struct
import sys 
import itertools

format_str = '=IHHIHI'
str_list = ['Size', 'Type', 'Channels', 'Rate', 'Bits', 'Data size']
slices = [
    slice(4, 8),
    slice(20, 22),
    slice(22, 24),
    slice(24, 28),
    slice(34, 36),
    slice(40, 44),
]

s = sys.stdin.buffer.read()

if len(s) < 44 or s[8:12] != b'WAVE':
    print('NO')
    exit()

s = b''.join([s[idx] for idx in slices])
results = struct.unpack(format_str, s)
print(', '.join([f'{str_list[i]}={results[i]}' for i in range(len(results))]))
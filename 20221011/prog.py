s1 = input().strip()

w = len(s1) - 2
h = 0
air = 0
water = 0
while ((s := input().strip()) != s1):
    if s == '#' + '.' * w + '#':
        air += w
    elif s == '#' + '~' * w + '#':
        water += w
    h += 1


new_h, new_w = w, h

md = water % new_w
water += new_w - md if md else 0
air -= new_w - md if md else 0


print('#' * (new_w + 2))
for i in range(air // new_w):
    print('#' + '.' * new_w + '#')
for i in range(water // new_w):
    print('#' + '~' * new_w + '#') 
print('#' * (new_w + 2))


if air > water:
    air_len = 20
    water_len = round(water * 20. / air)
else:
    water_len = 20
    air_len = round(air * 20 / water)

air_str = str(air) + '/' + str(air + water)
water_str = str(water) + '/' + str(air + water)

max_count_len = len(max([air_str, water_str], key=len))

print(f'{"*" * air_len : <20} {air_str : >{max_count_len}}')
print(f'{"~" * water_len : <20} {water_str : >{max_count_len}}')

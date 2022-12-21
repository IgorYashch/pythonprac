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

old_water = water
old_air = air

md = water % new_w
water += new_w - md if md else 0
air -= new_w - md if md else 0


print('#' * (new_w + 2))
for i in range(air // new_w):
    print('#' + '.' * new_w + '#')
for i in range(water // new_w):
    print('#' + '~' * new_w + '#') 
print('#' * (new_w + 2))


if old_air > old_water:
    air_len = 20
    water_len = round(old_water * 20. / old_air)
else:
    water_len = 20
    air_len = round(old_air * 20 / old_water)

air_str = str(old_air) + '/' + str(air + water)
water_str = str(old_water) + '/' + str(air + water)

max_count_len = len(max([air_str, water_str], key=len))

print(f'{"." * air_len : <20} {air_str : >{max_count_len}}')
print(f'{"~" * water_len : <20} {water_str : >{max_count_len}}')

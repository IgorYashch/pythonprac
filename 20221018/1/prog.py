s = input().lower()

count = len({s[i:i+2] for i in range(len(s)-1) if s[i: i + 2].isalpha()})

print(count)
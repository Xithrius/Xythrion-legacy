from modules.output import path
import random

with open(path('templates', 'text', 'X.txt'), 'r') as f:
    r = [list(x[:-1]) for x in f.readlines()]

for i in range(len(r)):
    for j in range(len(r[i])):
        if r[i][j] == 'x':
            r[i][j] = random.choice(['<', '>'])
for i in r:
    # print(f"{''.join(str(y) for y in i):<15}{>:15}")
    x = ''.join(str(y) for y in i)
    y = '--->'
    print(f"{x:<15}{y:>10}")

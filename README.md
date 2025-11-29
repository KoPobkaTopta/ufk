11: 
```
t1 = "╔═╤╗"
t2 = "║│"
t3 = "╟─┼╢"
t4 = "╚═╧╝"

W = int(input("Введите ширину W: "))
s0 = "*" * W
print(s0)

COLS = int(input("Введите число столбцов COLS: "))
s1 = ("|" + s0) * COLS + "|"
print(s1)

top_row = t1[0] + (t1[1] * W + t1[2]) * (COLS - 1) + t1[1] * W + t1[3]
print(top_row)

s2 = t2[0] + (" " * W + t2[1]) * (COLS - 1) + " " * W + t2[0]
print(s2)

s3 = t3[0] + (t3[1] * W + t3[2]) * (COLS - 1) + t3[1] * W + t3[3]
print(s3)

s4 = t4[0] + (t4[1] * W + t4[2]) * (COLS - 1) + t4[1] * W + t4[3]
print(s4)

H = int(input("Введите высоту H: "))
ROWS = int(input("Введите количество строк: "))

row_block = (s2 + "\n") * H

full_table = top_row + "\n" + (row_block + s3 + "\n") * (ROWS - 1) + row_block + s4

print(full_table)
```
12:
```
h = float(input())
w = float(input())

a = h / w
b = w / h

print(f"|{a}|{b}|")
```
13:
```
h = float(input())
w = float(input())

a = h / w
b = w / h

print(f"|{a:.4f}|{b:.4f}|")
```
14:
```
h = float(input())
w = float(input())

a = h / w
b = w / h

print(f"|{a:20.2f}|{b:20.2f}|")
```
15:
```
h = float(input())
w = float(input())

a = h / w
b = w / h

print(f"|{a:^20.2f}|{b:^20.2f}|")
```
16:
```
h = float(input())
w = float(input())

print(f"|{h / w:^20.2f}|{w / h:^20.2f}|")
```
17:
```
s = input()

if s[0] == '-':
    s = s[1:]


d1 = int(s[5])
d2 = int(s[4])
d3 = int(s[3])
d4 = int(s[2])
d5 = int(s[1])
d6 = int(s[0])

print(d1, d2, d3, d4, d5, d6)

total = d1 + d2 + d3 + d4 + d5 + d6
print("Сумма цифр:", total)
```
Домашняя работа:
1:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[0])
```
2:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[1])
```
3:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[-2])
```
4:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[-1])
```
5:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[9:20])
```
6:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[19:])
```
7:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[:10])
```
8:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[::2])
```
9:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[1::2])
```
10:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[1::3])
```
11:
```
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(s[::-1])
```
12:
```
names = ["Картофель", "Морковь", "Лук", "Капуста", "Свекла"]
amounts = [2.341, 0.873, 0.473, 3.762, 1.036]
prices = [79.36, 56.20, 39.01, 66.06, 72.99]

line = "-" * 79

print(line)
print(f"| {'Наименование товара':^27} | {'вес, кг':^9} | {'Цена, руб. / кг':^17} | {'Сумма, руб.':^13} |")
print(line)

grand_total = 0

for i in range(len(names)):
    name = names[i]
    weight = amounts[i]
    price = prices[i]
    
    cost = weight * price
    grand_total += cost
    
    print(f"| {name:<27} | {weight:>9.3f} | {price:>17.2f} | {cost:>13.2f} |")

print(line)

print(f"| {'ИТОГО:':<59} | {grand_total:>13.2f} |")
print(line)
```

```
import math

height = 100
gravity = 9.8
energy_per_bounce = 10
hours = 2

seconds_total = hours * 3600
time_fall = math.sqrt(2 * height / gravity)
time_cycle = time_fall * 2

bounces = 0
current_time = time_fall

# Условие изменено: учитываем, что шар должен успеть подняться (time_fall)
while current_time + time_fall <= seconds_total:
    bounces += 1
    current_time += time_cycle

total_energy = bounces * energy_per_bounce
print(int(total_energy))
```

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
```
s = "1Az3Sx4Dc6Fv7Gb9Hn2Pw3Tf5Et6Qn8Qy9Wu0Hm"
print(s[::3][::-1])
```

```
length = 5.2
width = 1.8
height = 1.4
box = 0.5

count_l = int(length / box)
count_w = int(width / box)
count_h = int(height / box)

total = count_l * count_w * count_h
print(total)
```
```
# Состав батончика
protein = 24
fat = 6
carbs = 42

# Считаем калории в одном батончике
# Белки и углеводы = 4 ккал, жиры = 9 ккал
bar_kcal = (protein * 4) + (fat * 9) + (carbs * 4)

# Лимиты
limit = 2500
eaten = 1670

# Сколько осталось свободного места
remaining = limit - eaten

# Считаем количество целых батончиков (целочисленное деление)
count = remaining // bar_kcal

print(count)
```
```
# Размеры кузова в см (4.5 м и 1.8 м)
car_length = 450
car_width = 180

# Размеры холодильника в см (основание)
fridge_size = 85

# Считаем, сколько влезает по длине и ширине
in_length = car_length // fridge_size
in_width = car_width // fridge_size

# Общая вместимость машины за 1 раз
capacity = in_length * in_width

# Всего нужно перевезти
total_fridges = 24

# Считаем количество поездок с ПОЛНОЙ загрузкой
# Используем целочисленное деление //
full_trips = total_fridges // capacity

print(full_trips)
```
```
names = ["Андрей", "Сергей", "Арсений", "Дмитрий", "Виталий"]
last_names = ["Иванов", "Петров", "Сидоров", "Андреев", "Сергеев"]

num = int(input())
idx = num - 1

name = names[idx][:-1] + "я"
surname = last_names[idx] + "а"

print(f"Уважаемые родители {name} {surname}! Приглашаем вас на родительское собрание, которое состоится 26 сентября в 19:00.")
print()
print("С уважением, классный руководитель")
```

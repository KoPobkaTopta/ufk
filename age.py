n = int(input())

if n % 100 >= 11 and n % 100 <= 14:
    print(n, "лет")
elif n % 10 == 1:
    print(n, "год")
elif n % 10 >= 2 and n % 10 <= 4:
    print(n, "года")
else:
    print(n, "лет")

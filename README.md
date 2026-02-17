```
class Date:
    sep = "/"

    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        if year < 100:
            year += 2000
        self.year = year

    def __str__(self):
        return f"{self.day:02d}{self.sep}{self.month:02d}{self.sep}{self.year:04d}"

    @staticmethod
    def str2num(date_string):
        for delimiter in ("/", "-", "."):
            if delimiter in date_string:
                return [int(part) for part in date_string.split(delimiter)]

    @classmethod
    def from_str(cls, date_string):
        day, month, year = cls.str2num(date_string)
        return cls(day, month, year)

    @staticmethod
    def isleap(year):
        if year % 400 == 0:
            return True
        if year % 100 == 0:
            return False
        if year % 4 == 0:
            return True
        return False

    def to_start(self):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.isleap(self.year):
            days_in_month[1] = 29
        return sum(days_in_month[:self.month - 1]) + self.day - 1


date1 = Date(1, 2, 2024)
print(date1)
print(f"{date1.to_start()} days passed")
print()
date2 = Date(31, 12, 2025)
print(date2)
print(f"{date2.to_start()} days passed")
```

Объяснение:

days_in_month — список с количеством дней в каждом месяце (по умолчанию 28 в феврале).

Если год високосный (проверяется через isleap()), февраль меняется на 29 дней.

sum(days_in_month[:self.month - 1]) — суммирует дни всех полных месяцев до текущего. Срез [:self.month - 1] берёт все месяцы перед нужным. Например, для февраля (month=2) срез [:1] берёт только январь — 31 день.

+ self.day - 1 — прибавляет дни текущего месяца, но вычитает 1, потому что считаются только полные прошедшие дни. 1 января — это 0 прошедших дней, а не 1.

Пример: 1 февраля 2024 → 31 (январь) + 1 - 1 = 31 день. 31 декабря 2025 → сумма дней с января по ноябрь + 31 - 1 = 364.

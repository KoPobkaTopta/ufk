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


print(f"1800: '{Date.isleap(1800)}'")
print(f"2024: '{Date.isleap(2024)}'")
```

Объяснение:

isleap() — статический метод (@staticmethod), потому что ему не нужен ни экземпляр (self), ни класс (cls). Он работает только с переданным аргументом year.

Логика проверки идёт по цепочке условий сверху вниз:

1. Если год делится на 400 без остатка — високосный (True). Например, 2000.
2. Если год делится на 100 без остатка — невисокосный (False). Например, 1800, 1900, 2100.
3. Если год делится на 4 без остатка — високосный (True). Например, 2024.
4. Всё остальное — невисокосный (False). Например, 2025.

Порядок проверок важен: сначала отсекаем кратные 400, потом кратные 100, потом кратные 4. Если переставить условия местами, результат будет неверным.

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

    def to_end(self):
        total = 366 if self.isleap(self.year) else 365
        return total - self.to_start() - 1


date = Date(1, 2, 24)
print(date)
print(date.to_end())
```

Объяснение:

to_end() считает, сколько полных дней осталось до конца года.

Сначала определяется общее количество дней в году: 366 для високосного, 365 для обычного.

Затем из общего количества вычитается to_start() (дни, прошедшие с начала года) и ещё 1 (сам текущий день).

Формула: total - to_start() - 1.

Пример: 1 февраля 2024 (високосный) → to_start() = 31, total = 366. Итого: 366 - 31 - 1 = 334. 31 декабря 2025 → to_start() = 364, total = 365. Итого: 365 - 364 - 1 = 0.

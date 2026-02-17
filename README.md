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


date = Date.from_str("08.03.25")
print(date)
```

Объяснение:

sep = "/" — свойство класса, хранит разделитель по умолчанию.

__init__ — конструктор. Если год меньше 100, прибавляет 2000 (25 → 2025).

__str__ — форматирует дату с ведущими нулями через :02d и :04d.

str2num() — статический метод (@staticmethod). Перебирает допустимые разделители ("/", "-", "."), находит нужный, разбивает строку через .split() и возвращает список чисел: "08.03.25" → [8, 3, 25].

from_str() — метод класса (@classmethod). Принимает cls — ссылку на класс. Вызывает cls.str2num() для разбора строки, затем создаёт новый объект через cls(day, month, year). Конструктор приводит год 25 к 2025, а __str__ выводит 08/03/2025.

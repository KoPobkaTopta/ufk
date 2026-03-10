from datetime import date as dt_date


class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year + 2000 if year < 100 else year

    def _to_date(self):
        return dt_date(self.year, self.month, self.day)

    def __str__(self):
        return f"{self.day:02d}/{self.month:02d}/{self.year}"

    def __sub__(self, other):
        return (self._to_date() - other._to_date()).days

    def __eq__(self, other):
        return self._to_date() == other._to_date()

    def __gt__(self, other):
        return self._to_date() > other._to_date()

    def __ge__(self, other):
        return self._to_date() >= other._to_date()


date1 = Date(8, 3, 2025)
date2 = Date(23, 2, 2025)

print(f"date1 = {date1}")
print(f"date2 = {date2}")
print(f"date1 > date2 >>> {date1 > date2}")

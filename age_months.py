n = int(input())

years = n // 12
months = n % 12

def year_word(y):
    if y % 100 >= 11 and y % 100 <= 14:
        return "лет"
    elif y % 10 == 1:
        return "год"
    elif y % 10 >= 2 and y % 10 <= 4:
        return "года"
    else:
        return "лет"

def month_word(m):
    if m % 100 >= 11 and m % 100 <= 14:
        return "месяцев"
    elif m % 10 == 1:
        return "месяц"
    elif m % 10 >= 2 and m % 10 <= 4:
        return "месяца"
    else:
        return "месяцев"

if years == 0:
    print(months, month_word(months))
elif months == 0:
    print(years, year_word(years), "ровно")
else:
    print(years, year_word(years), months, month_word(months))

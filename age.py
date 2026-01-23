n = int(input())

# Определяем правильное окончание для слова "год"
# Правила склонения:
# - 1, 21, 31, ... (кроме 11) → "год"
# - 2-4, 22-24, 32-34, ... (кроме 12-14) → "года"
# - остальные → "лет"

last_digit = n % 10
last_two_digits = n % 100

if last_two_digits >= 11 and last_two_digits <= 14:
    suffix = "лет"
elif last_digit == 1:
    suffix = "год"
elif last_digit >= 2 and last_digit <= 4:
    suffix = "года"
else:
    suffix = "лет"

print(f"{n} {suffix}")

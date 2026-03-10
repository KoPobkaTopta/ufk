class Animal:
    def __init__(self, breed, name, age):
        self.breed = breed
        self.name = name
        self.age = age

    def __str__(self):
        return (
            f"Это {self.breed}. Его зовут {self.name}. "
            f"Возраст - {self.age} лет."
        )

    def __eq__(self, other):
        return self.age == other.age

    def __gt__(self, other):
        return self.age > other.age

    def __ge__(self, other):
        return self.age >= other.age


alex = Animal("лев", "Алекс", 4)
marty = Animal("зебра", "Марти", 5)
skiper = Animal("пингвин", "Шкипер", 4)

print(f"alex age:  {alex.age}")
print(f"marty age:  {marty.age}")
print(f"skiper age:  {skiper.age}")

print()
print(f"alex > marty: {alex > marty}")
print(f"alex < marty: {alex < marty}")
print(f"alex = marty: {alex == marty}")

print()
print(f"alex > skiper: {alex > skiper}")
print(f"alex < skiper: {alex < skiper}")
print(f"alex = skiper: {alex == skiper}")

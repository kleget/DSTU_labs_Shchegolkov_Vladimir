class ComplexNumber:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imaginary - other.imaginary)

    def __lt__(self, other):
        return (self.real, self.imaginary) < (other.real, other.imaginary)

    def __gt__(self, other):
        return (self.real, self.imaginary) > (other.real, other.imaginary)

    def __eq__(self, other):
        return (self.real == other.real) and (self.imaginary == other.imaginary)

    def __str__(self):
        return f"{self.real} + {self.imaginary}i"


# Демонстрационная программа
c1 = ComplexNumber(3, 4)
c2 = ComplexNumber(1, 2)

result = c1 - c2
print(result)  # Вычитание

print(c1 < c2)  # Сравнение <
print(c1 > c2)  # Сравнение >
print(c1 == c2)  # Сравнение ==
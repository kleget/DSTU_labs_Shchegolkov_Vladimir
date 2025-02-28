class ComplexNumber:
    def __init__(self, real: float, imag: float):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        real_part = self.real * other.real - self.imag * other.imag
        imag_part = self.real * other.imag + self.imag * other.real
        return ComplexNumber(real_part, imag_part)

    def __truediv__(self, other):
        denominator = other.real ** 2 + other.imag ** 2
        real_part = (self.real * other.real + self.imag * other.imag) / denominator
        imag_part = (self.imag * other.real - self.real * other.imag) / denominator
        return ComplexNumber(real_part, imag_part)

    def __str__(self):
        return f"{self.real} + {self.imag}i"


class ComplexCollection:
    def __init__(self):
        self.numbers = []

    def add(self, complex_number: ComplexNumber):
        self.numbers.append(complex_number)

    def display(self):
        for num in self.numbers:
            print(num)

    def sum_all(self):
        result = ComplexNumber(0, 0)
        for num in self.numbers:
            result += num
        return result

    def subtract_all(self):
        if not self.numbers:
            return ComplexNumber(0, 0)
        result = self.numbers[0]
        for num in self.numbers[1:]:
            result -= num
        return result

    def multiply_all(self):
        if not self.numbers:
            return ComplexNumber(1, 0)
        result = self.numbers[0]
        for num in self.numbers[1:]:
            result *= num
        return result

    def divide_all(self):
        if not self.numbers:
            return ComplexNumber(1, 0)
        result = self.numbers[0]
        for num in self.numbers[1:]:
            result /= num
        return result


c1 = ComplexNumber(2, 3)
c2 = ComplexNumber(1, -4)
collection = ComplexCollection()
collection.add(c1)
collection.add(c2)
collection.display()
print("Сумма всех элементов:", collection.sum_all())
print("Разность всех элементов:", collection.subtract_all())
print("Произведение всех элементов:", collection.multiply_all())
print("Частное всех элементов:", collection.divide_all())

import math

class Shape:
    
    def area(self):
        pass
    
    def perimeter(self):
        pass
    
    def area_greater_than(self, other):
        return self.area() > other.area()
    
    def area_less_than(self, other):
        return self.area() < other.area()
    
    def perimeter_greater_than(self, other):
        return self.perimeter() > other.perimeter()
    
    def perimeter_less_than(self, other):
        return self.perimeter() < other.perimeter()

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side ** 2
    
    def perimeter(self):
        return 4 * self.side

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width
    
    def perimeter(self):
        return 2 * (self.length + self.width)

class Triangle(Shape):
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
    
    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))
    
    def perimeter(self):
        return self.side1 + self.side2 + self.side3

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius

def create_shape():
    print("\nВыберите тип фигуры:")
    print("1 - Квадрат")
    print("2 - Прямоугольник")
    print("3 - Треугольник")
    print("4 - Круг")
    
    choice = input("Введите номер: ")
    
    if choice == "1":
        side = float(input("Введите длину стороны: "))
        return Square(side)
    elif choice == "2":
        length = float(input("Введите длину: "))
        width = float(input("Введите ширину: "))
        return Rectangle(length, width)
    elif choice == "3":
        side1 = float(input("Введите первую сторону: "))
        side2 = float(input("Введите вторую сторону: "))
        side3 = float(input("Введите третью сторону: "))
        return Triangle(side1, side2, side3)
    elif choice == "4":
        radius = float(input("Введите радиус: "))
        return Circle(radius)
    else:
        print("Неверный выбор")
        return None

def compare_shapes():
    while True:
        print("\n=== Сравнение фигур ===")
        
        print("\nПервая фигура:")
        shape1 = create_shape()
        if shape1 is None:
            continue
        
        print("\nВторая фигура:")
        shape2 = create_shape()
        if shape2 is None:
            continue
        
        print(f"\nРезультаты:")
        print(f"Площадь 1: {shape1.area():.2f}")
        print(f"Площадь 2: {shape2.area():.2f}")
        print(f"Периметр 1: {shape1.perimeter():.2f}")
        print(f"Периметр 2: {shape2.perimeter():.2f}")
        
        print(f"\nСравнение площади:")
        if shape1.area_greater_than(shape2):
            print("Фигура 1 имеет большую площадь")
        elif shape1.area_less_than(shape2):
            print("Фигура 2 имеет большую площадь")
        else:
            print("Площади фигур равны")
        
        print(f"\nСравнение периметра:")
        if shape1.perimeter_greater_than(shape2):
            print("Фигура 1 имеет больший периметр")
        elif shape1.perimeter_less_than(shape2):
            print("Фигура 2 имеет больший периметр")
        else:
            print("Периметры фигур равны")
        
        again = input("\nСравнить еще фигуры? (y/n): ")
        if again.lower() != 'y':
            break

if __name__ == "__main__":
    compare_shapes()
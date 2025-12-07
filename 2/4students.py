class Person:
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def get_info(self):
        return f"Имя: {self.name}, Возраст: {self.age}"

class Student(Person):
   
    
    def __init__(self, name, age, group_number, average_grade):
        super().__init__(name, age)
        self.group_number = group_number
        self.average_grade = average_grade
    
    def calculate_scholarship(self):
        
        if self.average_grade == 5:
            return 6000
        elif self.average_grade < 5:
            return 4000
        else:
            return 0
    
    def get_scholarship_info(self):
        
        scholarship = self.calculate_scholarship()
        return f"Стипендия: {scholarship} руб."
    
    def scholarship_greater_than(self, other_student):
        
        return self.calculate_scholarship() > other_student.calculate_scholarship()
    
    def scholarship_less_than(self, other_student):
        
        return self.calculate_scholarship() < other_student.calculate_scholarship()
    
    def get_full_info(self):
        
        return f"{self.get_info()}, Группа: {self.group_number}, Средний балл: {self.average_grade}, {self.get_scholarship_info()}"

class GraduateStudent(Student):
    
    
    def __init__(self, name, age, group_number, average_grade, research_work):
        super().__init__(name, age, group_number, average_grade)
        self.research_work = research_work
    
    def calculate_scholarship(self):
        
        if self.average_grade == 5:
            return 8000
        elif self.average_grade < 5:
            return 6000
        else:
            return 0
    
    def get_full_info(self):
        
        base_info = super().get_full_info()
        return f"{base_info}, Научная работа: {self.research_work}"

def create_person():
    
    print("\nВыберите тип:")
    print("1 - Студент")
    print("2 - Аспирант")
    
    choice = input("Введите номер: ")
    
    name = input("Введите имя: ")
    age = int(input("Введите возраст: "))
    group = input("Введите номер группы: ")
    grade = float(input("Введите средний балл: "))
    
    if choice == "1":
        return Student(name, age, group, grade)
    elif choice == "2":
        research = input("Введите название научной работы: ")
        return GraduateStudent(name, age, group, grade, research)
    else:
        print("Неверный выбор")
        return None

def compare_scholarships():
    
    while True:
        print("\n=== Сравнение стипендий ===")
        
        print("\nПервый человек:")
        person1 = create_person()
        if person1 is None:
            continue
        
        print("\nВторой человек:")
        person2 = create_person()
        if person2 is None:
            continue
        
        print(f"\nРезультаты:")
        print(f"{person1.get_full_info()}")
        print(f"{person2.get_full_info()}")
        
        print(f"\nСравнение стипендий:")
        if person1.scholarship_greater_than(person2):
            print(f"{person1.name} получает большую стипендию")
        elif person1.scholarship_less_than(person2):
            print(f"{person2.name} получает большую стипендию")
        else:
            print("Стипендии равны")
        
        again = input("\nСравнить еще? (y/n): ")
        if again.lower() != 'y':
            break

if __name__ == "__main__":
    compare_scholarships()
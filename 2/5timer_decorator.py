import time
import os

def timer_decorator(func):
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  
        
        print(f"Функция {func.__name__} выполнилась за: {execution_time:.2f} мс")
        return result
    return wrapper

@timer_decorator
def add_numbers(a, b):

    result = a + b
    print(f"Результат сложения: {a} + {b} = {result}")
    return result

@timer_decorator
def process_file_operations(input_file, output_file):

    try:
    
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            a = float(lines[0].strip())
            b = float(lines[1].strip())
        
        result = a + b
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f"Входные числа: {a}, {b}\n")
            file.write(f"Результат вычисления: {a} + {b} = {result}\n")
        
        print(f"Файловые операции завершены! Результат записан в {output_file}")
        print(f"Путь к выходному файлу: {os.path.abspath(output_file)}")
        return result
        
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден")
        return None
    except ValueError:
        print("Ошибка: неверный формат данных в файле")
        return None
    

def test_function_1():
    
    print("\n=== Тест функции сложения ===")
    try:
        a = float(input("Введите первое число: "))
        b = float(input("Введите второе число: "))
        add_numbers(a, b)
    except ValueError:
        print("Ошибка: введите корректные числа")

def test_function_2():
    
    print("\n=== Тест файловых операций ===")
    
    if not os.path.exists('input.txt'):
        print("Файл input.txt не найден. Создание тестового файла...")
        try:
            a = float(input("Введите первое число для файла: "))
            b = float(input("Введите второе число для файла: "))
            
            with open('input.txt', 'w', encoding='utf-8') as file:
                file.write(f"{a}\n")
                file.write(f"{b}\n")
            print("Файл input.txt создан")
        except ValueError:
            print("Ошибка: введите корректные числа")
            return
    
    process_file_operations('input.txt', 'output.txt')
    
    if os.path.exists('output.txt'):
        print("\nСодержимое output.txt:")
        with open('output.txt', 'r', encoding='utf-8') as file:
            print(file.read())

def main():
    while True:
        print("\n=== Тестирование декоратора времени выполнения ===")
        print("1 - Тест функции сложения")
        print("2 - Тест файловых операций")
        print("3 - Выход")
        
        choice = input("Выберите вариант: ")
        
        if choice == "1":
            test_function_1()
        elif choice == "2":
            test_function_2()
        elif choice == "3":
            print("Программа завершена")
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()
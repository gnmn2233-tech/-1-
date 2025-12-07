def filter_strings(filter_func, string_list):

    return list(filter(filter_func, string_list))

def check_filter_input():
    
    while True:
        user_input = input("\nВведите строки для фильтрации (через запятую): ")
        
        if not user_input.strip():
            print("Поле ввода не может быть пустым. Пожалуйста, введите данные ещё раз.")
            continue
        
        # Разделение строк и удаление пробелов
        strings = [s.strip() for s in user_input.split(',')]
        
        print(f"\nИсходные строки: {strings}")
        
        # 1. Исключить строки с пробелами
        result1 = filter_strings(lambda s: ' ' not in s, strings)
        print(f"Без пробелов: {result1}")
        
        # 2. Исключить строки, начинающиеся с буквы 'a'
        result2 = filter_strings(lambda s: not s.lower().startswith('a'), strings)
        print(f"Без строк на 'a': {result2}")
        
        # 3. Исключить строки, длина которых меньше 5
        result3 = filter_strings(lambda s: len(s) >= 5, strings)
        print(f"Длина >= 5: {result3}")

        # 4. Исключить строки, удовлетворяющие всем условиям
        result4 = filter_strings(lambda s: ' ' not in s and not s.lower().startswith('a') and len(s) >= 5, strings)
        print(f"Все условия: {result4}")

if __name__ == "__main__":
    check_filter_input()
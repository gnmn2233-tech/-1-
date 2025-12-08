def is_palindrome(s):

    # Очистка строк: преобразование в строчные буквы, удаление символов, отличных от букв и цифр.
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    
    # Проверьте, является ли это палиндромом
    return cleaned == cleaned[::-1]

def check_palindrome_input():
    
    while True:
        user_input = input("\nВведите строку, которую вы хотите проверить: ")
        
        if not user_input.strip():
            print("Поле ввода не может быть пустым. Пожалуйста, введите данные ещё раз.")
            continue

        
        result = is_palindrome(user_input)
        
        if result:
            print(f"✓ '{user_input}' YES")
        else:
            print(f"✗ '{user_input}' NO")

if __name__ == "__main__":
    check_palindrome_input()
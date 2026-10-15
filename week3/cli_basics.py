# ============================================
# ОСНОВЫ ARGPARSE
# Первый CLI-инструмент
# ============================================

import argparse


def main():
    # Создаём парсер
    parser = argparse.ArgumentParser(
        description="Мой первый CLI-инструмент",
        epilog="Пример: python3 cli_basics.py Данил --age 25"
    )
    
    # Позиционный аргумент (обязательный)
    parser.add_argument(
        "name",
        help="Твоё имя"
    )
    
    # Опциональный аргумент
    parser.add_argument(
        "--age",
        type=int,
        default=0,
        help="Твой возраст (по умолчанию: 0)"
    )
    
    # Флаг
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Подробный вывод"
    )
    
    # Парсим аргументы
    args = parser.parse_args()
    
    # Используем
    print(f"Привет, {args.name}!")
    
    if args.age:
        print(f"Тебе {args.age} лет")
    
    if args.verbose:
        print(f"\n[DEBUG] Все аргументы: {args}")


if __name__ == "__main__":
    main()

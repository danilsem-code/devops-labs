# ============================================
# ИНФОРМАЦИЯ О СИСТЕМЕ (sys)
# Работа с аргументами и платформой
# ============================================

import sys
import platform
import os


def show_system_info():
    """Показывает информацию о системе."""
    print("=" * 70)
    print("ИНФОРМАЦИЯ О СИСТЕМЕ")
    print("=" * 70)
    
    print(f"🐍 Python:     {sys.version.split()[0]}")
    print(f"💻 Платформа:  {sys.platform}")
    print(f"🖥️  Система:   {platform.system()} {platform.release()}")
    print(f"🏗️  Архитектура: {platform.machine()}")
    print(f"👤 Пользователь: {os.environ.get('USER', 'неизвестно')}")
    print(f"🏠 Домашняя папка: {os.path.expanduser('~')}")
    print(f"📂 Текущая папка: {os.getcwd()}")
    print(f"🔧 Аргументы:  {sys.argv}")
    print("=" * 70)


if __name__ == "__main__":
    show_system_info()
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        print(f"\n📝 Ты передал аргументы: {sys.argv[1:]}")
        
        if sys.argv[1] == "--help":
            print("\nИспользование:")
            print("  python3 sys_info.py           # Информация о системе")
            print("  python3 sys_info.py --help    # Помощь")
    else:
        print("\n💡 Совет: запусти 'python3 sys_info.py --help'")

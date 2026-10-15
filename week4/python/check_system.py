#!/usr/bin/env python3
# ============================================
# PYTHON-СКРИПТ ДЛЯ ПРОВЕРКИ СИСТЕМЫ
# Вызывается из Bash
# ============================================

import sys
import platform
import os
import subprocess
from datetime import datetime


def main():
    """Главная функция."""
    print("=" * 60)
    print("🐍 PYTHON SYSTEM CHECK")
    print("=" * 60)
    
    # Информация о системе
    print(f"Хост:      {platform.node()}")
    print(f"Система:   {platform.system()} {platform.release()}")
    print(f"Python:    {sys.version.split()[0]}")
    print(f"Время:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Аргументы, переданные из Bash
    if len(sys.argv) > 1:
        print(f"\n📝 Аргументы из Bash: {sys.argv[1:]}")
    
    # Проверка диска
    print(f"\n💾 Использование диска:")
    try:
        result = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            print(f"   {lines[1]}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print("=" * 60)
    print("✅ Python-скрипт завершён успешно")
    
    # Возвращаем код 0 (успех)
    return 0


if __name__ == "__main__":
    sys.exit(main())

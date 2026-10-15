#!/bin/bash
# ============================================
# BASH-СКРИПТ, КОТОРЫЙ ВЫЗЫВАЕТ PYTHON
# ============================================

echo "============================================"
echo "🚀 BASH: Запуск Python-скрипта"
echo "============================================"

# 1. Проверяем, установлен ли Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен!"
    exit 1
fi

echo "✅ Python3 найден: $(which python3)"
echo ""

# 2. Запускаем Python-скрипт
echo "📞 Вызов Python-скрипта..."
echo ""

# Передаём аргументы в Python
python3 python/check_system.py "$@"

# 3. Проверяем код возврата
EXIT_CODE=$?

echo ""
echo "============================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Python-скрипт завершён успешно (код: $EXIT_CODE)"
else
    echo "❌ Python-скрипт завершён с ошибкой (код: $EXIT_CODE)"
fi
echo "============================================"

exit $EXIT_CODE

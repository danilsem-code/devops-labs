#!/bin/bash
# ============================================
# BASH: PING-СКАН СЕРВЕРОВ
# Вызывается из Python
# ============================================

if [ $# -eq 0 ]; then
    echo "❌ Использование: $0 host1 host2 ..."
    exit 1
fi

echo "🔍 Проверка серверов..."
echo ""

FAILED=0

for host in "$@"; do
    if ping -c 1 -W 2 "$host" > /dev/null 2>&1; then
        echo "✅ $host — доступен"
    else
        echo "❌ $host — НЕДОСТУПЕН"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "Итог: проверено $#, недоступно $FAILED"

# Возвращаем код 1, если есть недоступные
if [ $FAILED -gt 0 ]; then
    exit 1
fi

exit 0

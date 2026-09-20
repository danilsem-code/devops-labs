#!/bin/bash
# ============================================
# CHECK_SYSTEM.SH
# Итоговый скрипт первой недели DevOps
# Проверяет: серверы, диск, логи
# ============================================

# Настройки
LOG_DIR="$HOME/devops-labs/logs"
REPORT_FILE="$LOG_DIR/system_report_$(date +%Y-%m-%d).txt"
APP_LOG="$HOME/devops-labs/logs/app.log"
DISK_THRESHOLD=80  # порог заполнения диска в %

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# ============================================
# ФУНКЦИЯ: Проверка доступности сервера
# ============================================
check_server() {
    local host=$1
    if ping -c 1 -W 1 "$host" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $host доступен${NC}"
        return 0
    else
        echo -e "${RED}❌ $host недоступен${NC}"
        return 1
    fi
}

# ============================================
# ФУНКЦИЯ: Проверка места на диске
# ============================================
check_disk() {
    local disk_usage=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
    echo "Использование диска: ${disk_usage}%"
    
    if [ "$disk_usage" -gt "$DISK_THRESHOLD" ]; then
        echo -e "${RED}⚠️  ДИСК ЗАПОЛНЕН БОЛЕЕ ${DISK_THRESHOLD}%${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Место на диске в норме${NC}"
        return 0
    fi
}

# ============================================
# ФУНКЦИЯ: Поиск ошибок в логах
# ============================================
check_logs() {
    if [ ! -f "$APP_LOG" ]; then
        echo -e "${YELLOW}⚠️  Лог-файл не найден: $APP_LOG${NC}"
        return 1
    fi
    
    local error_count=$(grep -c "ERROR" "$APP_LOG" 2>/dev/null || echo 0)
    local warn_count=$(grep -c "WARN" "$APP_LOG" 2>/dev/null || echo 0)
    
    echo "Ошибок (ERROR): $error_count"
    echo "Предупреждений (WARN): $warn_count"
    
    if [ "$error_count" -gt 0 ]; then
        echo -e "${RED}⚠️  Обнаружены ошибки в логах!${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Ошибок в логах нет${NC}"
        return 0
    fi
}

# ============================================
# ОСНОВНАЯ ЧАСТЬ
# ============================================

echo "============================================"
echo "  DEVOPS SYSTEM CHECK"
echo "  $(date)"
echo "============================================"
echo ""

# Создаём папку для логов
mkdir -p "$LOG_DIR"

# Начинаем запись отчёта
{
    echo "============================================"
    echo "  ОТЧЁТ О СОСТОЯНИИ СИСТЕМЫ"
    echo "  Дата: $(date)"
    echo "============================================"
    echo ""
    
    # 1. Проверка серверов
    echo "--- [1] ПРОВЕРКА СЕРВЕРОВ ---"
    SERVERS=("yandex.ru" "vk.com" "gosuslugi.ru")
    SERVERS_OK=0
    SERVERS_FAIL=0
    
    for server in "${SERVERS[@]}"; do
        if check_server "$server"; then
            SERVERS_OK=$((SERVERS_OK + 1))
        else
            SERVERS_FAIL=$((SERVERS_FAIL + 1))
        fi
    done
    echo "Доступно: $SERVERS_OK из ${#SERVERS[@]}"
    echo ""
    
    # 2. Проверка диска
    echo "--- [2] ПРОВЕРКА ДИСКА ---"
    check_disk
    echo ""
    
    # 3. Проверка логов
    echo "--- [3] ПРОВЕРКА ЛОГОВ ---"
    check_logs
    echo ""
    
    # Итог
    echo "============================================"
    echo "  ИТОГ"
    echo "============================================"
    if [ "$SERVERS_FAIL" -eq 0 ]; then
        echo "✅ Все серверы доступны"
    else
        echo "❌ Недоступных серверов: $SERVERS_FAIL"
    fi
    
} | tee "$REPORT_FILE"

echo ""
echo "📄 Отчёт сохранён: $REPORT_FILE"
echo "============================================"

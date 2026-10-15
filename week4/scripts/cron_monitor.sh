#!/bin/bash
# ============================================
# МОНИТОРИНГ СИСТЕМЫ ПО РАСПИСАНИЮ
# Запускается из Cron каждые 5 минут
# ============================================

# Пути
BASE_DIR="$HOME/devops-labs/week4"
LOG_FILE="$BASE_DIR/logs/cron_monitor.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Логируем начало
echo "========================================" >> "$LOG_FILE"
echo "🔍 Мониторинг: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# 1. Собираем метрики через Python
cd "$BASE_DIR" || exit 1
python3 python/check_system.py >> "$LOG_FILE" 2>&1

# 2. Проверяем серверы
bash scripts/ping_servers.sh 8.8.8.8 1.1.1.1 >> "$LOG_FILE" 2>&1

# 3. Проверяем место на диске
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
echo "Disk usage: ${DISK_USAGE}%" >> "$LOG_FILE"

if [ "$DISK_USAGE" -gt 90 ]; then
    echo "⚠️  ДИСК ЗАПОЛНЕН: ${DISK_USAGE}%" >> "$LOG_FILE"
fi

echo "✅ Мониторинг завершён" >> "$LOG_FILE"

#!/bin/bash
# ============================================
# ПОЛНЫЙ ЦИКЛ: Bash → Python → Bash
# ============================================

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/full_check_$(date +%Y-%m-%d_%H-%M-%S).log"

mkdir -p "$LOG_DIR"

echo "============================================" | tee "$LOG_FILE"
echo "🔍 FULL SYSTEM CHECK: $(date)" | tee -a "$LOG_FILE"
echo "============================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 1. Python собирает метрики
echo "📊 Шаг 1: Сбор метрик (Python)" | tee -a "$LOG_FILE"
python3 python/check_system.py 2>&1 | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 2. Bash проверяет серверы
echo "🌐 Шаг 2: Проверка серверов (Bash)" | tee -a "$LOG_FILE"
bash scripts/ping_servers.sh 8.8.8.8 1.1.1.1 2>&1 | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 3. Python анализирует результаты
echo "📈 Шаг 3: Анализ (Python)" | tee -a "$LOG_FILE"
python3 python/run_ping.py 8.8.8.8 1.1.1.1 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "✅ Проверка завершена. Лог: $LOG_FILE" | tee -a "$LOG_FILE"

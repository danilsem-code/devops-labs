#!/bin/bash
# ============================================
# ПРОСТОЙ СКРИПТ ДЛЯ CRON
# ============================================

LOG_FILE="$HOME/devops-labs/week4/logs/cron_hello.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "$(date '+%Y-%m-%d %H:%M:%S') | Привет от Cron!" >> "$LOG_FILE"

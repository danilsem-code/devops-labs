#!/usr/bin/env python3
# ============================================
# DEVOPS TOOL v1.0
# Универсальный инструмент для мониторинга
# ============================================
#
# Использование:
#   python3 devops_tool.py check          # Проверить серверы
#   python3 devops_tool.py metrics        # Собрать метрики
#   python3 devops_tool.py report         # Показать отчёт
#   python3 devops_tool.py --help         # Помощь
# ============================================

import argparse
import subprocess
import platform
import logging
import sqlite3
import sys
import os
import re
import datetime
import yaml

try:
    import requests
except ImportError:
    requests = None


# ============================================
# ЗАГРУЗКА КОНФИГА
# ============================================

def load_config(filename="config.yaml"):
    """Загружает YAML-конфиг."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Конфиг {filename} не найден!")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Ошибка в YAML: {e}")
        sys.exit(1)


# ============================================
# ЛОГИРОВАНИЕ
# ============================================

def setup_logger(config, verbose=False):
    """Настраивает логгер."""
    log_config = config.get('logging', {})
    log_file = log_config.get('file', 'logs/devops_tool.log')
    log_level = logging.DEBUG if verbose else log_config.get('level', 'INFO')
    
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger("devops_tool")
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Не дублировать handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


# ============================================
# КОМАНДА: CHECK
# ============================================

def ping_host(host, timeout=2):
    """Проверяет доступность хоста."""
    param = '-n' if platform.system() == 'Windows' else '-c'
    try:
        result = subprocess.run(
            ['ping', param, '1', host],
            capture_output=True,
            timeout=timeout + 1
        )
        return result.returncode == 0
    except:
        return False


def cmd_check(args, config, logger):
    """Проверяет доступность серверов."""
    servers = config.get('servers', [])
    
    logger.info(f"🔍 Проверка {len(servers)} серверов...")
    
    results = []
    critical_failed = []
    
    for server in servers:
        name = server['name']
        host = server['host']
        is_critical = server.get('critical', False)
        
        is_up = ping_host(host)
        
        if is_up:
            logger.info(f"✅ {name} ({host}) — доступен")
        else:
            logger.error(f"❌ {name} ({host}) — НЕДОСТУПЕН")
            if is_critical:
                critical_failed.append(name)
        
        results.append((name, host, is_up))
    
    # Итог
    up = sum(1 for _, _, status in results if status)
    down = len(results) - up
    
    logger.info(f"\n{'=' * 60}")
    logger.info(f"ИТОГ: ✅ {up} доступно | ❌ {down} недоступно")
    
    if critical_failed:
        logger.critical(f"🚨 КРИТИЧНЫЕ СЕРВЕРЫ НЕДОСТУПНЫ: {', '.join(critical_failed)}")
        if args.exit_on_fail:
            sys.exit(1)
    
    logger.info(f"{'=' * 60}")


# ============================================
# КОМАНДА: METRICS
# ============================================

def get_cpu_usage():
    """Получает загрузку CPU (упрощённо)."""
    try:
        if platform.system() == "Darwin":
            result = subprocess.run(
                ["top", "-l", "1", "-n", "0"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split('\n'):
                if 'CPU usage' in line:
                    match = re.search(r'(\d+\.\d+)% user', line)
                    if match:
                        return float(match.group(1))
        return 0.0
    except:
        return 0.0


def get_disk_usage():
    """Получает загрузку диска."""
    try:
        result = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            return float(parts[4].replace('%', ''))
        return 0.0
    except:
        return 0.0


def init_db(config, logger):
    """Инициализирует БД."""
    db_path = config['database']['path']
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server TEXT NOT NULL,
            cpu REAL,
            ram REAL,
            disk REAL,
            timestamp TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    logger.debug(f"БД {db_path} инициализирована")


def cmd_metrics(args, config, logger):
    """Собирает метрики системы."""
    logger.info("📊 Сбор метрик системы...")
    
    init_db(config, logger)
    
    server_name = platform.node()
    cpu = get_cpu_usage()
    disk = get_disk_usage()
    ram = 50.0  # Заглушка для macOS
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Сохраняем в БД
    conn = sqlite3.connect(config['database']['path'])
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO metrics (server, cpu, ram, disk, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (server_name, cpu, ram, disk, timestamp))
    conn.commit()
    conn.close()
    
    logger.info(f"Сервер: {server_name}")
    logger.info(f"CPU:  {cpu}%")
    logger.info(f"RAM:  {ram}%")
    logger.info(f"Disk: {disk}%")
    
    # Проверяем пороги
    thresholds = config.get('thresholds', {})
    
    if cpu > thresholds.get('cpu', 80):
        logger.warning(f"⚠️  CPU превышает порог {thresholds['cpu']}%")
    if ram > thresholds.get('ram', 85):
        logger.warning(f"⚠️  RAM превышает порог {thresholds['ram']}%")
    if disk > thresholds.get('disk', 90):
        logger.warning(f"⚠️  Disk превышает порог {thresholds['disk']}%")
    
    logger.info("✅ Метрики сохранены")


# ============================================
# КОМАНДА: REPORT
# ============================================

def cmd_report(args, config, logger):
    """Показывает отчёт по метрикам."""
    logger.info("📈 Формирование отчёта...")
    
    db_path = config['database']['path']
    
    if not os.path.exists(db_path):
        logger.error(f"БД {db_path} не найдена. Запусти 'metrics' сначала.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Последние N записей
    limit = args.limit if hasattr(args, 'limit') else 10
    
    cursor.execute("""
        SELECT server, cpu, ram, disk, timestamp
        FROM metrics
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    
    print(f"\n{'=' * 80}")
    print(f"📊 ОТЧЁТ ПО МЕТРИКАМ (последние {len(rows)})")
    print(f"{'=' * 80}")
    print(f"{'Сервер':<20} {'CPU':>8} {'RAM':>8} {'Disk':>8}  {'Время'}")
    print(f"{'-' * 80}")
    
    for row in rows:
        print(f"{row[0]:<20} {row[1]:>7}% {row[2]:>7}% {row[3]:>7}%  {row[4]}")
    
    print(f"{'=' * 80}")
    
    # Статистика
    cursor.execute("""
        SELECT 
            COUNT(*),
            AVG(cpu),
            AVG(ram),
            AVG(disk),
            MAX(cpu),
            MAX(disk)
        FROM metrics
    """)
    
    stat = cursor.fetchone()
    
    print(f"\n📈 Статистика:")
    print(f"   Замеров: {stat[0]}")
    print(f"   CPU:  среднее {stat[1]:.1f}%, максимум {stat[4]:.1f}%")
    print(f"   RAM:  среднее {stat[2]:.1f}%")
    print(f"   Disk: среднее {stat[3]:.1f}%, максимум {stat[5]:.1f}%")
    
    conn.close()


# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================

def main():
    parser = argparse.ArgumentParser(
        description="DevOps Tool — универсальный инструмент мониторинга",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python3 devops_tool.py check                  # Проверить серверы
  python3 devops_tool.py check --exit-on-fail   # Для CI/CD
  python3 devops_tool.py metrics                # Собрать метрики
  python3 devops_tool.py report --limit 20      # Отчёт по 20 записям
        """
    )
    
    parser.add_argument("--config", default="config.yaml", help="Путь к конфигу")
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    
    subparsers = parser.add_subparsers(dest="command", help="Команды")
    
    # check
    check_parser = subparsers.add_parser("check", help="Проверить серверы")
    check_parser.add_argument("--exit-on-fail", action="store_true", help="Выход 1 при ошибке")
    
    # metrics
    metrics_parser = subparsers.add_parser("metrics", help="Собрать метрики")
    
    # report
    report_parser = subparsers.add_parser("report", help="Показать отчёт")
    report_parser.add_argument("--limit", type=int, default=10, help="Сколько записей")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Загружаем конфиг
    config = load_config(args.config)
    
    # Настраиваем логгер
    logger = setup_logger(config, args.verbose)
    
    # Выполняем команду
    if args.command == "check":
        cmd_check(args, config, logger)
    elif args.command == "metrics":
        cmd_metrics(args, config, logger)
    elif args.command == "report":
        cmd_report(args, config, logger)


if __name__ == "__main__":
    main()
